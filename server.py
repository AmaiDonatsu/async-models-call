from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.classes.model_utils import SigLIPModel, MsMarcoModel
from api.routes.call_models import CallModels
from contextlib import asynccontextmanager
from loguru import logger
import sys
from datetime import datetime
from api.utils.logging_config import setup_logging
import scripts.unblock_port_8000

scripts.unblock_port_8000.kill_process_on_port(8000)

setup_logging()

siglip_model = None
ms_marco_model = None

call_models_routes = CallModels(siglip_model, ms_marco_model)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the models on startup
    global siglip_model, ms_marco_model, call_models_routes
    siglip_model_path = "./models/siglip_onnx"
    ms_marco_model_path = "./models/ms-marco-onnx"
    
    # Load SigLIP
    try:
        siglip_model = SigLIPModel(siglip_model_path)
        call_models_routes.siglip_model = siglip_model
        logger.info(f"SigLIP model loaded successfully from {siglip_model_path}")
    except Exception as e:
        logger.error(f"Error loading SigLIP model: {e}")
        
    # Load MS MARCO
    try:
        ms_marco_model = MsMarcoModel(ms_marco_model_path)
        call_models_routes.ms_marco_model = ms_marco_model
        logger.info(f"MS MARCO model loaded successfully from {ms_marco_model_path}")
    except Exception as e:
        logger.error(f"Error loading MS MARCO model: {e}")
    yield
    # Clean up on shutdown if needed
    pass

app = FastAPI(title="Async Models Call API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(call_models_routes.router)


@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Async Models Call API"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed") 
    return {
        "status": "healthy",
        "siglip_loaded": siglip_model is not None,
        "ms_marco_loaded": ms_marco_model is not None
    }

@app.get("/error-test")
async def error_test():
    try:
        logger.info("Error test endpoint accessed")
        1 / 0
    except Exception as e:
        logger.error(f"¡Ups! Algo salió mal: {e}")
        return {"error": "Internal error"}

if __name__ == "__main__":
    logger.info("run in http://127.0.0.1:8000")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)