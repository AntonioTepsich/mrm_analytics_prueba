# services

Esta carpeta contiene la lógica principal para manejar la extracción de texto desde los archivos PDF, así como herramientas útiles para realizar estas operaciones. A continuación se describen los diferentes submódulos y sus propósitos:

### Subcarpetas y Archivos

#### **extractors**
Esta subcarpeta contiene la implementación de diferentes clases de extractores, que se encargan de extraer texto desde los archivos PDF. Los extractores heredan de una clase base (`BaseExtractor`) que define la estructura básica y la lógica común para la extracción. Cada extractor tiene un enfoque particular para manejar los archivos PDF:
- **base_extractor.py**: Clase abstracta que define los métodos comunes y la estructura para los extractores específicos. Gestiona la creación y limpieza de archivos temporales.
- **test1.py**: Implementa un extractor para documentos legales (Test 1), enfocándose en la identificación de párrafos y títulos.
- **test2.py**: Implementa un extractor que utiliza OCR para reconocer texto en imágenes de páginas PDF (Test 2). Realiza un preprocesamiento para mejorar la calidad del OCR.

#### **utils**
Esta subcarpeta contiene funciones útiles para operaciones recurrentes en el procesamiento de PDF.

#### **structure_manager.py**
Este archivo define la clase `StructureManager`, que se encarga de gestionar y registrar los diferentes extractores disponibles. Permite seleccionar el extractor adecuado según el tipo de archivo que se quiere procesar, facilitando la extensión a nuevos tipos de extractores sin modificar la estructura principal del código.

### Importancia
El módulo **services** centraliza la lógica de extracción y procesamiento de los archivos PDF, haciendo que el código sea modular, escalable y fácil de mantener. Cualquier nuevo extractor puede agregarse registrándolo en el `StructureManager`, lo cual hace que el sistema sea flexible y se pueda adaptar a diferentes tipos de documentos sin modificar el funcionamiento base.

