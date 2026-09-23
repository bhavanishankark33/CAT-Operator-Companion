from app.core.pipeline import build_counterfactual


class CounterfactualSkillCompiler:
    def compile(self, state_store):
        build_counterfactual(state_store)
        return state_store.state.counterfactual