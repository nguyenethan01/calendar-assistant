from datetime import datetime
from typing import Dict, Any, Optional
from .llm_service import LLMService

class NLPService:
    def __init__(self, timezone: str = 'America/Los_Angeles'):
        self.timezone = timezone
        self.llm = LLMService()

    def parse_event_creation(self, query: str) -> Dict[str, Any]:
        """
        Uses LLM to parse natural language query into event data.
        """
        try:
            return self.llm.parse_calendar_query(query)
        except Exception as e:
            raise ValueError(f"Failed to parse event creation query: {str(e)}")

    def validate_parsed_event(self, event: Dict[str, Any]) -> Optional[str]:
        """Validates the parsed event structure."""
        if not event or 'event' not in event:
            return "Invalid event structure"
            
        event_data = event['event']
        required_fields = ['summary', 'start', 'end']
        
        for field in required_fields:
            if field not in event_data:
                return f"Missing required field: {field}"
                
        return None 