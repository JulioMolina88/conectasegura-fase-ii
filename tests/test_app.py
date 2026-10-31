from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_prediction_valid_input() -> None:
    payload = {
        "frecuencia_llamadas_24h": 18,
        "duracion_minutos": 3.4,
        "reportes_previos": 2,
        "variacion_patron_llamadas": 1.1,
        "riesgo_red": 0.8,
        "actividad_nocturna": 0.0,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "probabilidad_fraude" in response.json()


def test_rejects_negative_duration() -> None:
    payload = {
        "frecuencia_llamadas_24h": 1,
        "duracion_minutos": -5,
        "reportes_previos": 0,
        "variacion_patron_llamadas": 0,
        "riesgo_red": 0,
        "actividad_nocturna": 0,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
