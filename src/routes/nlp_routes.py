from flask import Blueprint, request, jsonify
from services.llm_service import LLMService
from services.calendar_service import CalendarService

nlp_bp = Blueprint('nlp', __name__)
llm_service = LLMService()
calendar_service = CalendarService()

@nlp_bp.route('/create', methods=['POST'])
def create_from_natural_language():
    """Creates an event from a natural language query."""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing query in request'
            }), 400

        # Parse the natural language query
        parsed_event = llm_service.parse_calendar_query(data['query'])
        
        # Create the event using the calendar service
        created_event = calendar_service.create_event(parsed_event['event'])
        
        return jsonify({
            'status': 'success',
            'event': {
                'id': created_event['id'],
                'summary': created_event['summary'],
                'start': created_event['start'],
                'end': created_event['end'],
                'link': created_event.get('htmlLink', '')
            }
        })

    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 