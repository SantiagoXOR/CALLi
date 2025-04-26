from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import logging

from app.routers import campaign_router, call_router, cache_router, twilio_webhook_router, contact_router, report_router, audio_cache_router, auth_router
from app.api.endpoints import calls as calls_ws_router
from app.config.settings import get_settings
from app.services.cache_service import cache_service
from app.utils.logging import setup_logging, setup_app_logging
from app.middleware import setup_error_handling, setup_auth_middleware

# Inicializar configuración
settings = get_settings()

# Configurar directorio de logs
os.makedirs("logs", exist_ok=True)

# Configurar logger
logger = setup_logging(
    app_name="call-automation",
    level=settings.LOG_LEVEL,
    log_file="logs/app.log",
    console=True
)

# Definir el contexto de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Iniciar tarea de sincronización de caché al iniciar la aplicación
    logger.info("Starting cache sync task")
    await cache_service.start_sync_task()
    yield
    # Detener tarea de sincronización de caché al cerrar la aplicación
    logger.info("Stopping cache sync task")
    await cache_service.stop_sync_task()

app = FastAPI(
    title="Call Automation API",
    description="API para automatización de llamadas telefónicas",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Configurar logging para la aplicación
setup_app_logging(app, logger, exclude_paths=["/health", "/metrics", "/docs", "/redoc", "/openapi.json"])

# Configurar manejo de errores
setup_error_handling(app, logger)

# Configurar autenticación si está habilitada
if settings.AUTH_ENABLED:
    setup_auth_middleware(app)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Los eventos de inicio y cierre ahora se manejan con el contexto de vida (lifespan)

# Incluir rutas
from app.routers import call_webhook
app.include_router(campaign_router.router)
app.include_router(call_router.router)
app.include_router(cache_router.router)
app.include_router(calls_ws_router.router)
app.include_router(call_webhook.router, prefix="/api/v1/calls")
app.include_router(twilio_webhook_router.router, prefix="/api")
app.include_router(contact_router.router)
app.include_router(report_router.router)
app.include_router(audio_cache_router.router)
app.include_router(auth_router.router)

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de Automatización de Llamadas",
        "version": "1.0.0",
        "environment": settings.APP_ENV,
        "docs_url": "/docs" if settings.APP_ENV != "production" else None
    }
