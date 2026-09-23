from fastapi.testclient import TestClient

from app.core.store import store
from app.main import app


client = TestClient(app)


def setup_function():
    store.reset()


def test_worker_scenario_updates_shared_state_and_intervention():
    response = client.post("/api/simulate", json={"scenario": "WORKER_APPROACHING"})

    assert response.status_code == 200
    body = response.json()
    assert body["state"]["safety"]["risk"] == "HIGH"
    assert body["intentguard"]["predicted_action"] == "SWING_RIGHT"
    assert body["intervention"]["channel"] == "voice"
    assert client.get("/api/state").json()["safety"]["nearby_worker"] is True


def test_slow_cycles_start_and_complete_a_training_loop():
    response = client.post("/api/simulate", json={"scenario": "SLOW_CYCLES"})
    assert response.status_code == 200
    assert response.json()["state"]["performance"]["dominant_contributor"] == "SWING"

    started = client.post("/api/intervention/start", json={"skill": "swing_efficiency"}).json()
    completed = client.post(
        "/api/intervention/complete",
        json={"intervention_id": started["intervention_id"], "cycle_times": [35, 33, 32]},
    )

    assert completed.status_code == 200
    assert completed.json()["result"] == "positive"
    assert client.get("/api/training").json()[0]["status"] == "completed"


def test_diagnosis_is_grounded_and_unknown_symptom_is_not_invented():
    known = client.post("/api/diagnose", json={"symptom": "machine does not start"}).json()
    unknown = client.post("/api/diagnose", json={"symptom": "hydraulic noise"}).json()

    assert known["grounded"] is True
    assert unknown["grounded"] is False