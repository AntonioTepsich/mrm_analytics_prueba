# app/services/structure_manager.py

from .extractors.test1 import Test1Extractor
from .extractors.test2 import Test2Extractor

class StructureManager:
    """
    Clase para manejar y registrar diferentes extractores de estructuras de PDFs.
    """
    
    def __init__(self):
        self.extractors = {}
    
    def register_extractor(self, name: str, extractor_class, analyze_first_page=False):
        """
        Registrar un nuevo extractor.
        Args:
            name (str): Nombre del extractor.
            extractor_class: Clase del extractor.
            analyze_first_page (bool): Indica si el extractor debe analizar la primera página.
        """
        self.extractors[name] = {
            'class': extractor_class,
            'analyze_first_page': analyze_first_page
        }

    def get_extractor(self, name: str):
        """
        Obtener el extractor registrado por nombre.
        Args:
            name (str): Nombre del extractor.
        Returns:
            instance: Instancia del extractor registrado.
        """
        extractor_info = self.extractors.get(name)
        if not extractor_info:
            raise ValueError(f"No hay un extractor registrado con el nombre: {name}")
        
        extractor_class = extractor_info['class']
        analyze_first_page = extractor_info['analyze_first_page']
        return extractor_class(analyze_first_page=analyze_first_page)


# Instancia del gestor y registro de extractores disponibles
structure_manager = StructureManager()
structure_manager.register_extractor("test_1", Test1Extractor, analyze_first_page=True)
structure_manager.register_extractor("test_2", Test2Extractor, analyze_first_page=False)


