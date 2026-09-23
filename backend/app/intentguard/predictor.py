from app.core.pipeline import TRANSITIONS, predict_intent


class IntentGuard:
    def predict(self, state_store):
        return predict_intent(state_store)


__all__ = ["IntentGuard", "TRANSITIONS"]