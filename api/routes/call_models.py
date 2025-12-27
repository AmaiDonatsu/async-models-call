from api.classes.model_utils import SigLIPModel
from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from PIL import Image
import io
import json

class CallModels:
    def __init__(self, model):
        self.model = model
        self.router = APIRouter()
        self.router.add_api_route("/img-text-match", self.img_text_match, methods=["POST"])

    async def img_text_match(
        self,
        image: UploadFile = File(...),
        texts: str = Form(...) # Expecting a JSON string of list of texts
    ):
        if self.model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        try:
            # Read image
            image_content = await image.read()
            image_pil = Image.open(io.BytesIO(image_content)).convert("RGB")
            
            # Parse texts
            try:
                text_list = json.loads(texts)
                if not isinstance(text_list, list):
                    raise ValueError("texts must be a JSON list")
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON for texts")
            
            # Perform matching
            results = self.model.match(image_pil, text_list)
            
            return {"results": results}
    
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 