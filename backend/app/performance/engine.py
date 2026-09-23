from app.core.pipeline import analyze_performance


class PerformanceEngine:
    def analyze(self, state_store):
        analyze_performance(state_store)
        return state_store.state.performance