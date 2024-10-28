# models
Este archivo contiene la definición del modelo de respuesta para la API del proyecto. El objetivo principal es estructurar la salida de la aplicación, garantizando que la respuesta tenga un formato estándar y fácil de entender.

### Descripción de la Estructura del Modelo

- **`ExtractedTextResponse`**: Es una clase que hereda de `BaseModel` de Pydantic, lo que permite validar y serializar los datos de manera sencilla. Contiene un atributo:
  - `text` (str): Representa el texto extraído del archivo PDF.


### Importancia
Este modelo es importante porque asegura que todas las respuestas devueltas por la API tengan un formato coherente, facilitando la interpretación de los resultados por parte del cliente que realiza las solicitudes a la API.



