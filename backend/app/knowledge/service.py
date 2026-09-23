class KnowledgeService:
    """Small curated knowledge boundary; Gemini may rewrite, but not invent, it."""

    def answer(self, question: str, state) -> str:
        question_lower = question.lower()
        if "eta" in question_lower or "time" in question_lower:
            average = sum(state.performance.recent_cycle_times) / len(state.performance.recent_cycle_times)
            return (
                f"Your ETA is {state.task.eta_minutes:.0f} minutes because recent cycles average "
                f"{average:.1f} seconds, above the {state.task.baseline_cycle_time:.1f}-second baseline."
            )
        if "warning" in question_lower or "worker" in question_lower:
            return "The warning indicates a worker is approaching the predicted swing area. Hold movement until the area is clear."
        if "improve" in question_lower or "efficien" in question_lower:
            return "Focus on a smooth, shorter swing for the next three cycles. I will compare cycle time and swing duration with your baseline."
        return "I can explain the current ETA, safety warning, machine condition, or performance coaching from the live simulated state."

    def diagnose(self, symptom: str) -> dict:
        if "start" not in symptom.lower():
            return {"answer": "I do not have a verified guide for that symptom. Stop and request qualified service support.", "grounded": False}
        return {
            "answer": "Verify operator presence and displayed warnings, then check the basic start conditions in the provided machine guide. If unresolved, stop troubleshooting and request qualified service support.",
            "grounded": True,
            "source": "synthetic_curated_startup_guide",
        }

    def lesson(self, skill: str, counterfactual: dict | None) -> str:
        if counterfactual:
            return (
                f"Your recent cycle averaged {counterfactual['observed_metric']:.1f} seconds. "
                f"The {counterfactual['dominant_contributor'].lower()} phase added about "
                f"{counterfactual['estimated_excess_seconds']:.1f} seconds. For the next three cycles, "
                "use a smooth, shorter swing and I will verify the improvement."
            )
        return "For your next three cycles, keep the swing smooth and within your efficient range. Avoid unnecessary travel before dumping."