import requests
import json

url = "http://localhost:5000/detect"

data = {
    "query": "What is the capital of France?",
    "response": "Paris is possibly the capital, I think."
}

print("sending request to server...")

try:
    response = requests.post(url, json=data, timeout=60)
    
    print(f"\nstatus: {response.status_code}")
    print(f"\nresult:")
    print(json.dumps(response.json(), indent=2))
    
except Exception as e:
    print(f"error: {e}")