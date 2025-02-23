from flask import Blueprint, request, jsonify
from services.calendar_service import CalendarService

calendar_bp = Blueprint('calendar', __name__)
calendar_service = CalendarService(timezone='America/Los_Angeles')

@calendar_bp.route('/schedule', methods=['POST'])
def schedule_event():
    """Creates a calendar event from a pre-formatted payload."""
    try:
        data = request.get_json()
        
        # Validate payload structure
        if not data or 'event' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Invalid payload structure. Missing "event" object.'
            }), 400

        event = data['event']
        
        # Validate required fields
        required_fields = ['summary', 'start', 'end']
        missing_fields = [field for field in required_fields if field not in event]
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Create the event using our calendar service
        created_event = calendar_service.create_event(event)
        
        return jsonify({
            'status': 'success',
            'message': 'Event created successfully',
            'event': {
                'id': created_event['id'],
                'summary': created_event['summary'],
                'start': created_event['start'],
                'end': created_event['end'],
                'link': created_event.get('htmlLink', '')
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@calendar_bp.route('/events/upcoming', methods=['GET'])
def get_upcoming_events():
    """Gets the next 10 upcoming events."""
    try:
        events = calendar_service.get_upcoming_events()
        return jsonify({
            'status': 'success',
            'events': events
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 