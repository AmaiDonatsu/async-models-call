import requests
import json
from PIL import Image
import io
import numpy as np

def load_test_image(image_path="imgs/img1.png"):
    # Load image from path
    img = Image.open(image_path)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_match():
    url = "http://127.0.0.1:8000/img-text-match"
    
    # Prepare data
    img_path = "imgs/img1.png"
    img_bytes = load_test_image(img_path)
    texts = [ "women with long hair", "women standing","women with athletic build", "women stretching"]
    
    files = {
        'image': (img_path, img_bytes, 'image/png')
    }
    data = {
        'texts': json.dumps(texts)
    }
    
    try:
        print(f"Sending request to {url} with image {img_path}...")
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            print("Success!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_match()
