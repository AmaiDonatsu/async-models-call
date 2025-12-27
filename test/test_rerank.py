import requests
import json

def test_rerank():
    url = "http://127.0.0.1:8000/rerank"
    
    query = "How many people live in Berlin?"
    passages = [
        "Berlin has a population of 3.5 million people.",
        "The Eiffel Tower is in Paris.",
        "Germany is a country in Europe."
    ]
    
    data = {
        "query": query,
        "passages": json.dumps(passages)
    }
    
    print(f"Sending POST request to {url}...")
    try:
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print("Response received successfully!")
            results = response.json()
            print(json.dumps(results, indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_rerank()
