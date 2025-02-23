"""Route blueprints for the Calendar Assistant."""
from .calendar_routes import calendar_bp
from .health_routes import health_bp

__all__ = ['calendar_bp', 'health_bp'] 