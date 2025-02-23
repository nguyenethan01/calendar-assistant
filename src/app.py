from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables FIRST
load_dotenv()

# Then import routes that use those environment variables
from routes.calendar_routes import calendar_bp
from routes.health_routes import health_bp
from routes.nlp_routes import nlp_bp

def create_app():
    app = Flask(__name__)
    
    # Verify environment variables
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError("OPENAI_API_KEY environment variable is not set. Please add it to your .env file")
    
    # Register blueprints
    app.register_blueprint(calendar_bp, url_prefix='/calendar')
    app.register_blueprint(health_bp, url_prefix='/health')
    app.register_blueprint(nlp_bp, url_prefix='/nlp')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)