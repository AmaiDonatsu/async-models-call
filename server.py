from fastapi import FastAPI
import uvicorn
from api.classes.model_utils import SigLIPModel
from api.routes.call_models import CallModels
from contextlib import asynccontextmanager
from loguru import logger
import sys
from datetime import datetime
from api.utils.logging_config import setup_logging
import scripts.unblock_port_8000

scripts.unblock_port_8000.kill_process_on_port(8000)

setup_logging()

model = None

call_models_routes = CallModels(model)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model on startup
    global model, call_models_routes
    model_path = "./models/siglip_onnx"
    try:
        model = SigLIPModel(model_path)
        call_models_routes.model = model  # Actualizar el modelo en la instancia existente
        logger.info(f"Model loaded successfully from {model_path}")
        logger.info(f"call_models_routes.model: {call_models_routes.model}")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
    yield
    # Clean up on shutdown if needed
    pass

app = FastAPI(title="Async Models Call API", lifespan=lifespan)




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
        "model_loaded": model is not None
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