from app.schemas.contracts import Intervention, IntentPrediction, RiskLevel, SharedState


class CompanionOrchestrator:
    """Choose how the companion communicates; it never controls the machine."""

    _severity_rank = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}

    def decide(
        self,
        state: SharedState,
        intent: IntentPrediction,
        risk_predictions: list[dict],
    ) -> Intervention | None:
        highest_risk = self._highest_risk(state.safety.risk, intent.risk, risk_predictions)
        if highest_risk in ("HIGH", "CRITICAL"):
            if intent.consequence == "potential_worker_intersection":
                return Intervention(
                    level=3,
                    channel="voice",
                    message="Warning. Worker approaching your right swing area. Hold movement until the area is clear.",
                    reason="predicted_worker_intersection",
                    expires_in_sec=8,
                )
            return Intervention(
                level=3,
                channel="voice",
                message="Critical operating risk detected. Hold movement and confirm the area is clear.",
                reason="critical_operating_risk",
                expires_in_sec=8,
            )
        if highest_risk == "MEDIUM":
            return Intervention(
                level=1,
                channel="dashboard",
                message=state.safety.active_alert or "A medium-risk condition needs attention.",
                reason="risk_condition",
            )
        if state.performance.deviation:
            return Intervention(
                level=1,
                channel="dashboard",
                message="Cycle time is above your recent efficient baseline; the swing phase is the main contributor.",
                reason="performance_deviation",
            )
        return None

    def _highest_risk(
        self,
        safety_risk: RiskLevel,
        intent_risk: RiskLevel,
        predictions: list[dict],
    ) -> RiskLevel:
        risks = [safety_risk, intent_risk] + [item.get("severity", "LOW") for item in predictions]
        return max(risks, key=lambda risk: self._severity_rank.get(risk, 0))


companion = CompanionOrchestrator()