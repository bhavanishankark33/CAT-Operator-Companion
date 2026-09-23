from app.core.pipeline import analyze_risk


class RiskEngine:
    def analyze(self, state_store, intent):
        return analyze_risk(state_store, intent)