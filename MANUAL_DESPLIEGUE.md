# Manual de despliegue - ConectaSegura

## 1. Propósito

ConectaSegura es una API académica para clasificar el riesgo de llamadas telefónicas potencialmente fraudulentas. La solución utiliza un modelo de bosque aleatorio y expone servicios REST mediante FastAPI.

El proyecto fue contenerizado con Docker para asegurar portabilidad, consistencia de dependencias y ejecución reproducible en un entorno local o en la nube.

## 2. Arquitectura de la solución

La arquitectura sigue un modelo cliente-servidor:

```text
Cliente / Swagger UI
        ↓
API REST FastAPI
        ↓
Modelo de bosque aleatorio
        ↓
Respuesta JSON con clasificación, probabilidad y recomendación

La API incluye los siguientes endpoints:
- GET /: confirma que la API está activa.
- GET /health: verifica el estado del servicio y del modelo cargado.
- POST /predict: recibe variables de una llamada y devuelve la predicción.
- GET /docs: interfaz Swagger para probar los endpoints de forma visual.
3. Requerimientos técnicos
Para ejecutar el proyecto se requiere:
- Docker Desktop instalado y activo.
- Git instalado.
- Visual Studio Code o un editor de código.
- Conexión a internet durante la primera construcción de la imagen.
- Puerto local 8000 disponible.
4. Estructura del repositorio
conectasegura-fase-ii/
├── app.py
├── train_model.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── README.md
├── MANUAL_DESPLIEGUE.md
└── tests/
    └── test_app.py

5. Construcción de la imagen Docker
Desde la carpeta raíz del proyecto se ejecuta:
docker build -t conectasegura-api:1.0 .

Este proceso realiza las siguientes actividades:
1. Descarga una imagen base ligera de Python.
2. Instala las dependencias declaradas en requirements.txt.
3. Ejecuta train_model.py para entrenar y guardar el modelo.
4. Copia la API FastAPI al contenedor.
5. Expone el puerto 8000.
6. Genera la imagen conectasegura-api:1.0.
6. Ejecución local del contenedor
Para iniciar el servicio se utiliza:
docker run --name conectasegura-api -p 8000:8000 conectasegura-api:1.0

La opción -p 8000:8000 conecta el puerto 8000 de la computadora con el puerto 8000 del contenedor.

Cuando la API está activa, se puede acceder a:
http://localhost:8000/docs

Para detener el contenedor se presiona:
Ctrl + C

7. Prueba del endpoint de salud
El endpoint de estado se consulta mediante:
GET http://localhost:8000/health

Respuesta esperada:
{
  "status": "ok",
  "model": "Bosque aleatorio - ConectaSegura"
}

Una respuesta HTTP 200 confirma que la API está disponible y que el modelo se cargó correctamente.
8. Prueba de predicción
El endpoint POST /predict recibe seis variables relacionadas con el comportamiento de una llamada:
- frecuencia_llamadas_24h
- duracion_minutos
- reportes_previos
- variacion_patron_llamadas
- riesgo_red
- actividad_nocturna
Ejemplo de solicitud:
{
  "frecuencia_llamadas_24h": 18,
  "duracion_minutos": 3.4,
  "reportes_previos": 2,
  "variacion_patron_llamadas": 1.1,
  "riesgo_red": 0.8,
  "actividad_nocturna": 0.0
}

La API devuelve una respuesta con:
- Clasificación de la llamada.
- Etiqueta legitima o potencialmente_fraudulenta.
- Probabilidad estimada de fraude.
- Umbral operativo de 0.35.
- Recomendación operativa.
9. Validación de entradas
La API aplica validaciones antes de enviar datos al modelo.

Ejemplos:
- Una duración negativa produce una respuesta HTTP 422.
- Una duración de 1440 minutos se acepta como caso límite válido.
- Valores fuera de los rangos permitidos son rechazados con un mensaje descriptivo.
Estas validaciones reducen el riesgo de que datos incorrectos afecten la predicción.
10. Estrategia de despliegue en nube
La estrategia recomendada es utilizar un modelo PaaS compatible con contenedores.

Flujo propuesto:
Repositorio GitHub
        ↓
Servicio PaaS con Docker
        ↓
Construcción automática de la imagen
        ↓
Despliegue de la API FastAPI
        ↓
URL pública protegida mediante HTTPS

El servicio PaaS deberá configurarse para:
- Construir la aplicación desde el Dockerfile.
- Exponer el puerto 8000 o el puerto asignado por la plataforma.
- Mantener variables sensibles fuera del código fuente.
- Registrar errores y solicitudes.
- Monitorear disponibilidad, latencia y respuestas HTTP.
- Implementar escalamiento y actualización controlada del modelo cuando sea necesario.
11. Seguridad y operación
Para una implementación productiva se recomienda:
- Evitar almacenar información personal de los usuarios en los registros.
- Utilizar cifrado en tránsito mediante HTTPS.
- Gestionar secretos y credenciales con variables de entorno.
- Limitar el acceso a la API mediante autenticación.
- Supervisar errores, disponibilidad y posibles cambios en el desempeño del modelo.
- Mantener revisión humana para alertas de fraude de alto riesgo.
12. Uso de IA generativa para documentación
Se utilizó una herramienta de IA generativa como apoyo para estructurar este manual técnico, organizar los pasos de despliegue y redactar las secciones de arquitectura, pruebas y operación.

Ejemplo de prompt utilizado:
Actúa como especialista en MLOps. Redacta un manual técnico para desplegar una API FastAPI de detección de llamadas fraudulentas mediante Docker. Incluye requisitos, construcción de imagen, ejecución local, endpoints, pruebas, estrategia PaaS, seguridad y monitoreo.

El contenido generado fue revisado y adaptado al funcionamiento real de ConectaSegura.
13. Conclusión
La contenerización de ConectaSegura permite ejecutar la API y el modelo de forma consistente en diferentes entornos. La solución fue validada localmente mediante Docker y Swagger UI, demostrando comunicación funcional entre la API y el modelo de clasificación.

La arquitectura propuesta permite una futura migración a un entorno PaaS, manteniendo prácticas de portabilidad, monitoreo, seguridad y documentación técnica.