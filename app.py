"""API REST para estimar el riesgo de fraude de una llamada."""
from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


MODEL_PATH = Path("model/modelo_conectasegura.joblib")

if not MODEL_PATH.exists():
    raise RuntimeError("No se encontro el modelo. Ejecuta primero: python train_model.py")

artifact = joblib.load(MODEL_PATH)
model = artifact["model"]
FEATURES = artifact["features"]

app = FastAPI(
    title="ConectaSegura API",
    version="1.0.0",
    description="API academica para clasificar el riesgo de llamadas fraudulentas.",
)


class LlamadaEntrada(BaseModel):
    frecuencia_llamadas_24h: float = Field(..., ge=0, le=1000)
    duracion_minutos: float = Field(..., ge=0, le=1440)
    reportes_previos: float = Field(..., ge=0, le=1000)
    variacion_patron_llamadas: float = Field(..., ge=-20, le=20)
    riesgo_red: float = Field(..., ge=-20, le=20)
    actividad_nocturna: float = Field(..., ge=-20, le=20)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model": "Bosque aleatorio - ConectaSegura"}


@app.post("/predict")
def predict(llamada: LlamadaEntrada) -> dict:
    values = np.array([[getattr(llamada, feature) for feature in FEATURES]])
    probability = float(model.predict_proba(values)[0, 1])
    threshold = 0.35
    prediction = int(probability >= threshold)

    return {
        "llamada_fraudulenta": prediction,
        "etiqueta": "potencialmente_fraudulenta" if prediction else "legitima",
        "probabilidad_fraude": round(probability, 4),
        "umbral_operativo": threshold,
        "recomendacion": "Enviar a revision humana" if prediction else "Sin alerta prioritaria",
    }


@app.get("/")
def root() -> dict:
    return {"message": "ConectaSegura API activa. Consulta /docs para probar los endpoints."}
