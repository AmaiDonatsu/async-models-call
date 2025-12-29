import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

def test_security():
    print("--- Verificando Seguridad ---")
    
    print("\n1. Probando acceso desde IP local...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

    # Probando con un Origin no permitido
    print("\n2. Probando con Origin no permitido (unauthorized.com)...")
    try:
        headers = {"Origin": "https://unauthorized.com"}
        response = requests.get(f"{BASE_URL}/", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

    domain_allowed = os.getenv("ASYNC_CONTROL_DOMAIN")
    if domain_allowed:
        print(f"\n3. Probando con Origin permitido ({domain_allowed})...")
        try:
            origin_header = domain_allowed if domain_allowed.startswith("http") else f"https://{domain_allowed}"
            headers = {"Origin": origin_header}
            response = requests.get(f"{BASE_URL}/", headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("\n3. ASYNC_CONTROL_DOMAIN no configurado en .env, saltando prueba.")

if __name__ == "__main__":
    test_security()
