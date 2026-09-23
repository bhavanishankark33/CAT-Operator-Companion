from app.core.pipeline import understand_situation


class SituationEngine:
    def analyze(self, state_store):
        return understand_situation(state_store)