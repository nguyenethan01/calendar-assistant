from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timezone
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def test_auth():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('calendar', 'v3', credentials=creds)
        
        # Get the current time in RFC3339 format
        now = datetime.now(timezone.utc).isoformat()
        
        # List the next 10 upcoming events
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,  # Only get events from now onwards
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"Event: {event['summary']}, Start: {start}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    test_auth() 