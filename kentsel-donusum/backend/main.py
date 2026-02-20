import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import router as v1_router
from app.api.v1.admin import router as admin_router
from app.api.v1.gecmis_vakalar import router as vaka_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Kentsel Dönüşüm Karar Destek", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def genel_hata_handler(request: Request, exc: Exception):
    logger.error(f"Beklenmedik hata: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "hata": "Sistem hatası oluştu. Lütfen tekrar deneyin.",
            "istek_id": request.headers.get("X-Request-ID", "N/A")
        }
    )

app.include_router(v1_router)
app.include_router(admin_router)
app.include_router(vaka_router)
