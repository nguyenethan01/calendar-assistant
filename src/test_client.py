import requests
import json

def test_schedule_event():
    url = "http://localhost:5000/schedule"
    
    # Test payload
    payload = {
        "query": "schedule a 1 hour event today for cleaning room that has a deadline of tonight"
    }
    
    try:
        response = requests.post(url, json=payload)
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running?")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_schedule_event() 