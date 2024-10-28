# tests/test_pdf_extraction.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

testeo="tests/test1"
# testeo="tests/test2"

def test_extract_pdf_success():
    # Prueba con un PDF de ejemplo
    with open(testeo+".pdf", "rb") as pdf_file:
        response = client.post("/api/v1/extract-pdf", files={"file": pdf_file})
        assert response.status_code == 200
        
        extracted_text = response.json()["text"]
        assert len(extracted_text.strip()) > 0, "El texto extraído está vacío"

def test_extract_pdf_no_file():
    # Prueba cuando no se envía ningún archivo
    response = client.post("/api/v1/extract-pdf")
    assert response.status_code == 422  # 422 es el código de error para entrada inválida

def test_extract_pdf_invalid_file():
    # Prueba con un archivo no PDF (ej: un archivo de texto)
    with open(testeo+".txt", "rb") as txt_file:
        response = client.post("/api/v1/extract-pdf", files={"file": txt_file})
        assert response.status_code == 500  # Se espera un error porque no se puede extraer texto de un archivo no válido

