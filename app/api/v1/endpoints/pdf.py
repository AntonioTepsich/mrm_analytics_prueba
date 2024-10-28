from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from services.structure_manager import structure_manager
from models.response import ExtractedTextResponse

router = APIRouter()

@router.post("/extract-pdf", response_model=ExtractedTextResponse)
async def extract_pdf(file: UploadFile = File(...), type: str = Form(...)):
    # Verificar si el archivo se ha proporcionado
    if not file:
        raise HTTPException(status_code=400, detail="No se proporcionó ningún archivo")

    # Verificar que el archivo sea un PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="El archivo proporcionado no es un PDF")

    try:
        # Obtener el extractor adecuado utilizando el tipo proporcionado por el usuario
        extractor = structure_manager.get_extractor(type)
        
        # Extraer el texto utilizando el extractor seleccionado
        text = extractor.extract_text(file)
        
        return ExtractedTextResponse(text=text)
    
    except ValueError as e:
        # Si no se encuentra un extractor válido, devolver un error 400
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        # Si hay algún error durante el procesamiento, devolver un error 500
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")