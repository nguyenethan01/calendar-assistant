import pytest
from datetime import datetime
import json
from src.services.llm_service import LLMService

@pytest.fixture
def llm_service():
    return LLMService()

@pytest.mark.parametrize("query", [
    pytest.param(
        "Set up a cleaning session tomorrow morning at 9am",
        id="morning_cleaning"
    ),
    pytest.param(
        "Schedule dentist appointment next Friday at 2pm",
        id="dentist_appointment"
    ),
    pytest.param(
        "Create an event for grocery shopping this Saturday at 3pm",
        id="grocery_shopping"
    ),
    pytest.param(
        "Meeting with John on Monday at 10am for 45 minutes",
        id="meeting_with_duration"
    )
])
def test_valid_calendar_queries(query, llm_service):
    """Test that valid calendar queries are parsed correctly."""
    try:
        result = llm_service.parse_calendar_query(query)
        
        # Verify structure
        assert 'event' in result
        event = result['event']
        assert all(key in event for key in ['summary', 'start', 'end'])
        
        # Print parsed result for debugging
        print(f"\nQuery: {query}")
        print(f"Parsed result: {json.dumps(result, indent=2)}")
        
    except Exception as e:
        pytest.fail(f"Failed to parse valid query: '{query}'\nError: {str(e)}")

@pytest.mark.parametrize("query", [
    pytest.param(
        "maybe do something sometime",
        id="vague_time"
    ),
    pytest.param(
        "schedule an event",
        id="vague_purpose"
    ),
    pytest.param(
        "asdfghjkl",
        id="nonsense"
    ),
    pytest.param(
        "",
        id="empty"
    )
])
def test_invalid_calendar_queries(query, llm_service):
    """Test that invalid calendar queries raise appropriate errors."""
    with pytest.raises(ValueError) as exc_info:
        result = llm_service.parse_calendar_query(query)
    
    # Print error for debugging
    print(f"\nQuery: '{query}'")
    print(f"Error: {str(exc_info.value)}")

def test_parse_calendar_query_structure(llm_service):
    """Test that the LLM returns properly structured JSON."""
    query = "Schedule a meeting tomorrow at 2pm for one hour to clean my room"
    
    result = llm_service.parse_calendar_query(query)
    
    # Check basic structure
    assert isinstance(result, dict)
    assert 'event' in result
    
    event = result['event']
    # Check required fields
    assert 'summary' in event
    assert 'start' in event
    assert 'end' in event
    
    # Check datetime fields
    for field in ['start', 'end']:
        assert 'dateTime' in event[field]
        assert 'timeZone' in event[field]
        # Verify ISO format
        datetime.fromisoformat(event[field]['dateTime'].replace('Z', '+00:00'))

def test_parse_calendar_query_content(llm_service):
    """Test that the LLM extracts meaningful content."""
    query = "Schedule a team meeting next Monday at 3pm for 30 minutes"
    
    result = llm_service.parse_calendar_query(query)
    event = result['event']
    
    # Check that title is meaningful
    assert len(event['summary']) > 0
    assert 'team meeting' in event['summary'].lower()
    
    # Check timezone
    assert event['start']['timeZone'] == 'America/Los_Angeles'
    assert event['end']['timeZone'] == 'America/Los_Angeles'
    
    # Check that end time is after start time
    start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
    end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
    assert end > start

def test_parse_calendar_query_variations(llm_service):
    """Test different query formats."""
    test_queries = [
        "Set up a cleaning session tomorrow morning",
        "Schedule dentist appointment next Friday at 2pm",
        "Create an event for grocery shopping this weekend",
        "Meeting with John on Monday at 10am for 45 minutes"
    ]
    
    for query in test_queries:
        result = llm_service.parse_calendar_query(query)
        assert llm_service._validate_response(result)

def test_response_validation(llm_service):
    """Test the validation function."""
    valid_response = {
        "event": {
            "summary": "Test Event",
            "start": {
                "dateTime": "2024-03-19T14:00:00-07:00",
                "timeZone": "America/Los_Angeles"
            },
            "end": {
                "dateTime": "2024-03-19T15:00:00-07:00",
                "timeZone": "America/Los_Angeles"
            }
        }
    }
    
    invalid_responses = [
        {},  # Empty
        {"event": {}},  # Missing required fields
        {  # Missing timezone
            "event": {
                "summary": "Test",
                "start": {"dateTime": "2024-03-19T14:00:00"},
                "end": {"dateTime": "2024-03-19T15:00:00"}
            }
        }
    ]
    
    assert llm_service._validate_response(valid_response)
    
    for response in invalid_responses:
        assert not llm_service._validate_response(response) 