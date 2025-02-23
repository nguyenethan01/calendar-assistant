from openai import OpenAI
import os
from typing import Dict, Any
import json
from datetime import datetime

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def parse_calendar_query(self, query: str) -> Dict[str, Any]:
        """
        Uses GPT-3.5-turbo to parse natural language into structured data.
        """
        system_prompt = """
        You are a calendar assistant that helps parse natural language queries into structured data.
        You should extract event details and return them in a JSON format.
        
        Handle time references flexibly:
        - Specific times ("at 3pm"): Use as provided
        - Time ranges ("morning"): Use 9am
        - Part of day ("evening"): Use 6pm
        - Just date ("this weekend"): Use 10am
        - No time specified: Use next available time slot starting at the next hour
        
        Default duration if not specified:
        - Shopping/errands: 2 hours
        - Meetings: 1 hour
        - Appointments: 1 hour
        - General tasks: 1 hour
        
        Only throw errors if the query:
        - Is empty: "Query cannot be empty"
        - Has no clear purpose: "Query must specify an event purpose"
        - Is nonsensical: "Query is not a valid calendar request"
        
        For valid queries, return JSON with this structure:
        {
            "event": {
                "summary": "string",
                "description": "string",
                "start": {
                    "dateTime": "ISO-8601 string",
                    "timeZone": "America/Los_Angeles"
                },
                "end": {
                    "dateTime": "ISO-8601 string",
                    "timeZone": "America/Los_Angeles"
                }
            }
        }

        For invalid queries, return JSON with this structure:
        {
            "error": "error message string"
        }
        """

        user_prompt = f"""
        Parse this calendar query: "{query}"
        Current time: {datetime.now().isoformat()}
        
        A valid query needs:
        1. A clear purpose or title
        2. A specific time or date reference
        3. An explicit or implied duration
        
        Return the JSON response.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0,
                response_format={ "type": "json_object" }
            )
            
            # Parse the response
            result = json.loads(response.choices[0].message.content)
            
            # Check if the response contains an error
            if 'error' in result:
                raise ValueError(result['error'])
                
            # Validate the response structure
            if not self._validate_response(result):
                raise ValueError("Invalid response structure from LLM")
                
            return result

        except json.JSONDecodeError:
            raise ValueError("Failed to parse LLM response")
        except Exception as e:
            raise ValueError(f"Failed to parse query with LLM: {str(e)}")
    
    def _validate_response(self, response: Dict[str, Any]) -> bool:
        """Validates the LLM response has the correct structure."""
        try:
            event = response.get('event', {})
            required_fields = ['summary', 'start', 'end']
            
            for field in required_fields:
                if field not in event:
                    return False
                    
            # Validate datetime fields
            for field in ['start', 'end']:
                if 'dateTime' not in event[field] or 'timeZone' not in event[field]:
                    return False
                    
            return True
            
        except Exception:
            return False 