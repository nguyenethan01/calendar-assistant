import requests
import json
from typing import Dict, Any
from datetime import datetime

class CalendarClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url

    def create_event_from_query(self, query: str) -> Dict[str, Any]:
        """
        Sends a natural language query to create a calendar event.
        
        Example:
            client.create_event_from_query("Schedule a meeting tomorrow at 2pm for one hour")
        """
        try:
            response = requests.post(
                f"{self.base_url}/nlp/create",
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("\nEvent created successfully!")
                print(f"Title: {result['event']['summary']}")
                print(f"Start: {result['event']['start']['dateTime']}")
                print(f"End: {result['event']['end']['dateTime']}")
                print(f"Calendar Link: {result['event'].get('link', 'Not available')}")
                return result
            else:
                error_msg = response.json().get('message', 'Unknown error occurred')
                print(f"\nError: {error_msg}")
                return None
                
        except requests.exceptions.ConnectionError:
            print("\nError: Could not connect to server. Is it running?")
            return None
        except Exception as e:
            print(f"\nError: {str(e)}")
            return None

def main():
    client = CalendarClient()
    
    print("\nWelcome to Calendar Assistant!")
    print("Type 'quit' to exit")
    
    while True:
        print("\nWhat would you like to schedule?")
        query = input("> ").strip()
        
        if query.lower() == 'quit':
            break
            
        if query:
            client.create_event_from_query(query)
        else:
            print("Please enter a query or type 'quit' to exit")

if __name__ == "__main__":
    main() 