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
        Uses GPT-3.5-turbo to parse natural language into structured calendar data.
        """
        system_prompt = """
        You are a calendar assistant that helps parse natural language queries into structured data.
        You should extract event details and return them in a JSON format.
        Only respond with valid JSON, no other text.
        
        The JSON should have this structure:
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
        """

        user_prompt = f"""
        Parse this calendar query: "{query}"
        Current time: {datetime.now().isoformat()}
        
        Extract:
        1. Event title/summary
        2. Start time and date
        3. Duration or end time
        4. Any other relevant details for description
        
        Return only the JSON.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0,  # Make it deterministic
                response_format={ "type": "json_object" }  # Ensure JSON response
            )
            
            # Parse the response
            result = json.loads(response.choices[0].message.content)
            
            # Validate the response structure
            if not self._validate_response(result):
                raise ValueError("Invalid response structure from LLM")
                
            return result

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