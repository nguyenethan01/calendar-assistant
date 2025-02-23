from flask import Flask
from routes.calendar_routes import calendar_bp
from routes.health_routes import health_bp

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(calendar_bp, url_prefix='/calendar')
    app.register_blueprint(health_bp, url_prefix='/health')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)