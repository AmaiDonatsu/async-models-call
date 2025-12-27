import os
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

def export_model():
    model_id = "cross-encoder/ms-marco-MiniLM-L6-v2"
    save_directory = "models/ms-marco-onnx"
    
    print(f"Exporting {model_id} to {save_directory}...")
    
    # Export to ONNX
    model = ORTModelForSequenceClassification.from_pretrained(model_id, export=True)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    # Save the model and tokenizer
    model.save_pretrained(save_directory)
    tokenizer.save_pretrained(save_directory)
    
    print("Export complete!")

if __name__ == "__main__":
    export_model()
