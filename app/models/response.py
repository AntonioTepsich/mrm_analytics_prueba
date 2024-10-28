# app/models/response.py
from pydantic import BaseModel

class ExtractedTextResponse(BaseModel):
    text: str
