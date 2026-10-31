# Reporte de validación y pruebas — ConectaSegura

## 1. Objetivo

El objetivo de las pruebas fue comprobar que la API ConectaSegura funciona correctamente dentro de un contenedor Docker, que el modelo se carga de forma adecuada y que los endpoints responden tanto a solicitudes válidas como a datos inválidos.

## 2. Entorno de pruebas

| Elemento | Configuración utilizada |
|---|---|
| Sistema de ejecución | Docker Desktop |
| Imagen Docker | `conectasegura-api:1.0` |
| Framework de la API | FastAPI |
| Servidor | Uvicorn |
| Documentación interactiva | Swagger UI |
| URL local | `http://localhost:8000/docs` |
| Modelo | Bosque Aleatorio |
| Caso de uso | Clasificación de riesgo de llamadas fraudulentas |

## 3. Casos de prueba ejecutados

### Prueba 1. Construcción de imagen Docker

**Comando ejecutado:**

```bash
docker build -t conectasegura-api:1.0 .

Resultado esperado: crear la imagen Docker, instalar las dependencias y generar el modelo.

Resultado obtenido: la construcción finalizó correctamente y se generó la imagen conectasegura-api:1.0.

Estado: Aprobada.
Prueba 2. Verificación de disponibilidad
Endpoint probado:
GET /health

Resultado esperado: respuesta HTTP 200 con el estado de la API y el nombre del modelo.

Resultado obtenido:
{
  "status": "ok",
  "model": "Bosque aleatorio - ConectaSegura"
}

Estado: Aprobada.

La prueba confirma que el contenedor está en ejecución y que el modelo fue cargado correctamente.
Prueba 3. Predicción con datos válidos
Endpoint probado:
POST /predict

Datos enviados:
{
  "frecuencia_llamadas_24h": 18,
  "duracion_minutos": 3.4,
  "reportes_previos": 2,
  "variacion_patron_llamadas": 1.1,
  "riesgo_red": 0.8,
  "actividad_nocturna": 0.0
}

Resultado obtenido:
{
  "llamada_fraudulenta": 0,
  "etiqueta": "legitima",
  "probabilidad_fraude": 0.3486,
  "umbral_operativo": 0.35,
  "recomendacion": "Sin alerta prioritaria"
}

Estado: Aprobada.

La probabilidad obtenida fue de 0.3486, valor menor al umbral operativo de 0.35; por ello, la llamada se clasificó como legítima.
Prueba 4. Validación de dato inválido
Endpoint probado:
POST /predict

Dato inválido enviado:
{
  "duracion_minutos": -5
}

Resultado esperado: rechazar el dato con un error de validación HTTP 422.

Resultado obtenido: la API devolvió HTTP 422 Unprocessable Entity e indicó que duracion_minutos debe ser mayor o igual a cero.

Estado: Aprobada.

Esta prueba demuestra que la API protege el modelo ante valores fuera del rango permitido.
Prueba 5. Validación de valor límite
Endpoint probado:
POST /predict

Datos enviados:
{
  "frecuencia_llamadas_24h": 1,
  "duracion_minutos": 1440,
  "reportes_previos": 0,
  "variacion_patron_llamadas": 0,
  "riesgo_red": 0,
  "actividad_nocturna": 0
}

Resultado esperado: aceptar el valor máximo permitido para duracion_minutos y responder con HTTP 200.

Resultado obtenido:
{
  "llamada_fraudulenta": 0,
  "etiqueta": "legitima",
  "probabilidad_fraude": 0.3117,
  "umbral_operativo": 0.35,
  "recomendacion": "Sin alerta prioritaria"
}

Estado: Aprobada.

La prueba confirma que la API acepta correctamente el límite superior definido de 1440 minutos.
4. Resumen de resultados
Prueba	Resultado esperado	Resultado obtenido	Estado
Construcción Docker	Imagen creada	Imagen conectasegura-api:1.0 creada correctamente	Aprobada
GET /health	HTTP 200	Estado ok y modelo disponible	Aprobada
POST /predict válido	HTTP 200	Predicción generada correctamente	Aprobada
Dato negativo	HTTP 422	Error de validación recibido	Aprobada
Valor límite válido	HTTP 200	Predicción generada correctamente	Aprobada


5. Análisis
Las pruebas realizadas comprueban la integración entre Docker, FastAPI y el modelo de clasificación. La aplicación puede construirse y ejecutarse de manera reproducible mediante un contenedor.

La validación de entradas es importante porque evita que valores inválidos lleguen al modelo. Además, la prueba de valor límite confirma que las restricciones definidas en la API permiten procesar datos válidos dentro del rango establecido.
6. Limitaciones y recomendaciones
El modelo utilizado tiene fines académicos y fue entrenado con datos sintéticos. Antes de utilizar una solución similar en un entorno real, se recomienda:
- Entrenar con datos históricos y representativos.
- Incorporar autenticación en el endpoint de predicción.
- Usar HTTPS en un despliegue público.
- Monitorear errores, latencia y desempeño del modelo.
- Establecer un proceso periódico de revisión y reentrenamiento.
- Mantener supervisión humana para casos con riesgo elevado.
7. Conclusión
La API ConectaSegura cumplió las pruebas funcionales definidas. La imagen Docker se construyó correctamente, el contenedor ejecutó la aplicación, el endpoint de salud confirmó la disponibilidad del modelo y el endpoint de predicción respondió adecuadamente ante datos válidos, inválidos y valores límite.

Por lo tanto, la solución cuenta con una base funcional para su despliegue futuro en una plataforma de nube compatible con Docker.