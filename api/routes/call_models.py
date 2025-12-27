from api.classes.model_utils import SigLIPModel, MsMarcoModel
from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from PIL import Image
import io
import json

class CallModels:
    def __init__(self, siglip_model=None, ms_marco_model=None):
        self.siglip_model = siglip_model
        self.ms_marco_model = ms_marco_model
        self.router = APIRouter()
        self.router.add_api_route("/img-text-match", self.img_text_match, methods=["POST"])
        self.router.add_api_route("/rerank", self.rerank, methods=["POST"])

    async def img_text_match(
        self,
        image: UploadFile = File(...),
        texts: str = Form(...) # Expecting a JSON string of list of texts
    ):
        if self.siglip_model is None:
            raise HTTPException(status_code=503, detail="SigLIP model not loaded")
        
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
            results = self.siglip_model.match(image_pil, text_list)
            
            return {"results": results}
    
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def rerank(
        self,
        query: str = Form(...),
        passages: str = Form(...) # Expecting a JSON string of list of passages
    ):
        if self.ms_marco_model is None:
            raise HTTPException(status_code=503, detail="MS MARCO model not loaded")
            
        try:
            # Parse passages
            try:
                passage_list = json.loads(passages)
                if not isinstance(passage_list, list):
                    raise ValueError("passages must be a JSON list")
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON for passages")
                
            # Perform reranking
            results = self.ms_marco_model.rerank(query, passage_list)
            
            return {"query": query, "results": results}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
 