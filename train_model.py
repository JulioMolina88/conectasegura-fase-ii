"""Entrena y guarda el modelo demostrativo de ConectaSegura.

El conjunto de datos es sintetico y se usa solo con fines academicos.
"""
from pathlib import Path

import joblib
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier


FEATURES = [
    "frecuencia_llamadas_24h",
    "duracion_minutos",
    "reportes_previos",
    "variacion_patron_llamadas",
    "riesgo_red",
    "actividad_nocturna",
]


def main() -> None:
    X, y = make_classification(
        n_samples=6000,
        n_features=len(FEATURES),
        n_informative=5,
        n_redundant=1,
        weights=[0.85, 0.15],
        class_sep=1.0,
        flip_y=0.03,
        random_state=42,
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X, y)

    output_dir = Path("model")
    output_dir.mkdir(exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES}, output_dir / "modelo_conectasegura.joblib")
    print("Modelo guardado en model/modelo_conectasegura.joblib")


if __name__ == "__main__":
    main()
