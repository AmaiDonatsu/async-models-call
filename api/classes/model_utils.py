import os
import numpy as np
import onnxruntime as ort
from PIL import Image
from transformers import AutoProcessor, AutoTokenizer

class SigLIPModel:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.onnx_model_path = os.path.join(model_path, "model.onnx")
        
        # Load processor and tokenizer from the model directory
        self.processor = AutoProcessor.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        # Initialize ONNX Runtime session
        self.session = ort.InferenceSession(self.onnx_model_path, providers=['CPUExecutionProvider'])

    def preprocess_image(self, image: Image.Image):
        # SigLIP expects specific preprocessing
        inputs = self.processor(images=image, return_tensors="np")
        return inputs["pixel_values"]

    def preprocess_text(self, texts: list[str]):
        # Tokenize texts
        inputs = self.tokenizer(texts, return_tensors="np", padding="max_length", truncation=True)
        return inputs["input_ids"]

    def match(self, image: Image.Image, texts: list[str]):
        pixel_values = self.preprocess_image(image)
        input_ids = self.preprocess_text(texts)
        
        # Prepare inputs for ONNX session
        # We need to know the input names. Usually they are 'pixel_values' and 'input_ids'
        # Let's check session inputs
        input_names = [i.name for i in self.session.get_inputs()]
        
        ort_inputs = {
            "pixel_values": pixel_values,
            "input_ids": input_ids
        }
        
        # Perform inference
        outputs = self.session.run(None, ort_inputs)
        
        # SigLIP outputs are usually logits for image-text matching
        # Depending on the model export, it might return image_embeds and text_embeds
        # or direct logits. Assuming it returns logits based on the common SigLIP architecture
        # being used for zero-shot classification.
        
        logits_per_image = outputs[0] # [batch_size, num_texts]
        
        # Apply softmax to get probabilities
        probs = self._softmax(logits_per_image, axis=-1)
        
        results = []
        for i, text in enumerate(texts):
            results.append({
                "text": text,
                "score": float(probs[0, i])
            })
            
        return results

    def _softmax(self, x, axis=None):
        x_max = np.max(x, axis=axis, keepdims=True)
        exp_x = np.exp(x - x_max)
        return exp_x / np.sum(exp_x, axis=axis, keepdims=True)
