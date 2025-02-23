from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']

class CalendarService:
    def __init__(self, timezone='America/Los_Angeles'):
        self.timezone = timezone
        self._service = None

    def get_service(self):
        """Get an authorized Calendar API service instance."""
        if self._service:
            return self._service

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

        self._service = build('calendar', 'v3', credentials=creds)
        return self._service

    def create_event(self, event_data):
        """Creates a calendar event."""
        service = self.get_service()
        return service.events().insert(calendarId='primary', body=event_data).execute()

    def get_upcoming_events(self, max_results=10):
        """Gets the upcoming events."""
        service = self.get_service()
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', []) 