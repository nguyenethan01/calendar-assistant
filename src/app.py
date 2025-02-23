from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os.path
import pickle

app = Flask(__name__)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Get an authorized Calendar API service instance."""
    creds = None
    
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

@app.route('/schedule', methods=['POST'])
def schedule_event():
    """
    Endpoint to schedule events based on natural language input
    Example request body:
    {
        "query": "schedule a 1 hour event today for cleaning room that has a deadline of tonight"
    }
    """
    try:
        data = request.get_json()
        query = data.get('query')
        
        # TODO: Add language model integration here to parse the query
        # For now, let's just create a simple event
        
        service = get_calendar_service()
        
        # Simple example - creates event for current time + 1 hour
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=1)
        
        event = {
            'summary': 'Clean Room',
            'description': 'Auto-scheduled cleaning task',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Your/Timezone',  # e.g., 'America/New_York'
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Your/Timezone',  # e.g., 'America/New_York'
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return jsonify({
            'status': 'success',
            'message': 'Event created successfully',
            'eventId': event.get('id')
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)