from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer
import torch

def test_onnx_model():
    model_path = "models/ms-marco-onnx"
    
    print(f"Loading ONNX model from {model_path}...")
    model = ORTModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    # Inputs (Same as original test)
    queries = ['How many people live in Berlin?', 'How many people live in Berlin?']
    passages = [
        'Berlin has a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers.', 
        'New York City is famous for the Metropolitan Museum of Art.'
    ]
    
    features = tokenizer(queries, passages, padding=True, truncation=True, return_tensors="pt")
    
    # Inference
    print("Running inference...")
    with torch.no_grad():
        outputs = model(**features)
        scores = outputs.logits
        print("ONNX Scores:")
        print(scores)
        
    print("\nComparison Check:")
    print(f"Score for correct answer: {scores[0][0]:.4f}")
    print(f"Score for wrong answer: {scores[1][0]:.4f}")
    
    if scores[0][0] > scores[1][0]:
        print("\nSUCCESS: The model correctly ranked the relevant passage higher.")
    else:
        print("\nFAILURE: The model did not rank the relevant passage higher.")

if __name__ == "__main__":
    test_onnx_model()
