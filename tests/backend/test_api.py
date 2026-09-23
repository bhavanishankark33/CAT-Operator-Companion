from fastapi.testclient import TestClient

from app.core.store import store
from app.core.gemini import gemini
from app.main import app


client = TestClient(app)


def setup_function():
    store.reset()
    gemini.keys = []


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
    assert client.get("/api/counterfactual").json()["verification_status"] == "positive"
    assert client.get("/api/state").json()["performance"]["recent_cycle_times"] == [35.0, 33.0, 32.0]


def test_analysis_and_scenario_catalog_support_the_demo_flow():
    client.post("/api/reset")
    client.post("/api/simulate", json={"scenario": "WORKER_APPROACHING"})
    analysis = client.get("/api/analysis").json()
    scenarios = client.get("/api/scenarios").json()["scenarios"]

    assert analysis["situation"]["situation"] == "worker_approaching_operating_machine"
    assert analysis["risk_predictions"][0]["type"] == "PREDICTED_WORKER_INTERSECTION"
    assert "SLOW_CYCLES" in scenarios
    assert "MACHINE_START_FAILURE" in scenarios


def test_repeated_safety_condition_does_not_spam_alerts():
    client.post("/api/simulate", json={"scenario": "WORKER_APPROACHING"})
    client.post("/api/simulate", json={"scenario": "WORKER_APPROACHING"})

    alerts = client.get("/api/alerts").json()
    events = client.get("/api/events").json()
    assert len(alerts) == 1
    assert [event["type"] for event in events[:2]] == ["WORKER_APPROACHING", "WORKER_APPROACHING"]
    assert client.get("/api/operator-profile/OP001").status_code == 200


def test_diagnosis_is_grounded_and_unknown_symptom_is_not_invented():
    known = client.post("/api/diagnose", json={"symptom": "machine does not start"}).json()
    unknown = client.post("/api/diagnose", json={"symptom": "hydraulic noise"}).json()

    assert known["grounded"] is True
    assert unknown["grounded"] is False


def test_voice_contract_works_without_external_voice_api_or_gemini_key():
    response = client.post("/api/voice/tool", json={"question": "Why did my ETA increase?"})
    config = client.get("/api/voice/config")

    assert response.status_code == 200
    assert response.json()["speech_text"]
    assert response.json()["source"] == "deterministic_fallback"
    assert config.json() == {
        "provider": "deepgram_with_browser_fallback",
        "available": True,
        "deepgram_available": True,
        "browser_fallback_available": True,
        "format": "audio/mpeg",
    }