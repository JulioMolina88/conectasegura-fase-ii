# ConectaSegura - Fase II

API REST contenerizada para estimar el riesgo de llamadas fraudulentas.

## Estructura

```text
fase_ii_conectasegura/
├── app.py                 # API FastAPI
├── train_model.py         # Entrenamiento reproducible
├── requirements.txt       # Dependencias
├── Dockerfile             # Construccion de la imagen
├── .dockerignore          # Archivos excluidos de la imagen
├── model/
│   └── modelo_conectasegura.joblib
└── tests/
    └── test_app.py        # Pruebas funcionales y caso extremo
```

## Ejecucion local sin Docker

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python train_model.py
uvicorn app:app --reload
```

Abre `http://127.0.0.1:8000/docs` para probar la API.

## Docker

```bash
docker build -t conectasegura-api:1.0 .
docker run --name conectasegura-api -p 8000:8000 conectasegura-api:1.0
```

Consulta `http://localhost:8000/docs` y `http://localhost:8000/health`.

## Prueba de prediccion con curl

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"frecuencia_llamadas_24h":18,"duracion_minutos":3.4,"reportes_previos":2,"variacion_patron_llamadas":1.1,"riesgo_red":0.8,"actividad_nocturna":0.0}'
```
