from abc import ABC, abstractmethod
import tempfile
import shutil
import os
from fastapi import UploadFile  # Importa UploadFile si estás usando FastAPI

class BaseExtractor(ABC):
    def __init__(self, analyze_first_page=False):
        self.analyze_first_page = analyze_first_page

    @abstractmethod
    def _process_pdf(self, temp_pdf_path: str, analyze_first_page: bool) -> str:
        """Método abstracto para procesar un PDF dado su archivo temporal."""
        pass

    def extract_text(self, pdf_file: UploadFile) -> str:
        """Método público que maneja la creación y limpieza del archivo temporal, y el manejo de errores."""
        temp_pdf_path = ""

        try:
            temp_pdf_path = self._save_temp_pdf(pdf_file)
            return self._process_pdf(temp_pdf_path, self.analyze_first_page)
        except Exception as e:
            self._handle_processing_error(e)
        finally:
            self._cleanup_temp_pdf(temp_pdf_path)

    def _save_temp_pdf(self, pdf_file) -> str:
        """Guarda el archivo PDF en un archivo temporal y devuelve su ruta."""
        try:
            return self._create_temp_file(pdf_file)
        except Exception as e:
            raise Exception(f"Error al guardar el archivo temporal: {str(e)}")

    def _create_temp_file(self, pdf_file) -> str:
        """Crea un archivo temporal y copia el contenido del PDF cargado."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(pdf_file.file, tmp)
            return tmp.name

    def _cleanup_temp_pdf(self, temp_pdf_path: str):
        """Limpia el archivo PDF temporal."""
        if temp_pdf_path:
            self._delete_temp_file(temp_pdf_path)

    def _delete_temp_file(self, temp_pdf_path: str):
        """Elimina un archivo temporal si existe."""
        try:
            os.remove(temp_pdf_path)
        except Exception:
            pass

    def _handle_processing_error(self, error: Exception):
        """Maneja los errores que ocurren durante el procesamiento del PDF."""
        raise Exception(f"Error al procesar el archivo: {str(error)}")

