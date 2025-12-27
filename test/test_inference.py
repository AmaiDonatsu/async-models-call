import requests
import json
from PIL import Image
import io
import numpy as np

def create_dummy_image():
    # Create a 100x100 red image
    img = Image.new('RGB', (100, 100), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_match():
    url = "http://127.0.0.1:8000/img-text-match"
    
    # Prepare data
    img_bytes = create_dummy_image()
    texts = ["a red square", "a blue square", "a green square"]
    
    files = {
        'image': ('test.jpg', img_bytes, 'image/jpeg')
    }
    data = {
        'texts': json.dumps(texts)
    }
    
    try:
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
