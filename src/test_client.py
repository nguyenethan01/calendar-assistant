import requests
import json

def test_schedule_event():
    url = "http://localhost:5000/schedule"
    
    # Test payload
    payload = {
        "query": "schedule a 1 hour event today for cleaning room that has a deadline of tonight"
    }
    
    headers = {
        'Content-Type': 'application/json'  # Add this header
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("Status Code:", response.status_code)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Error:", response.text)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running?")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_schedule_event() 