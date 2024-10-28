# app/main.py
from fastapi import FastAPI
from api.v1.endpoints.pdf import router as pdf_router
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las solicitudes, puedes restringirlo a tu dominio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(pdf_router, prefix=settings.API_V1_STR)
