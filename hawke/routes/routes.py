from flask import Flask
from routes.admin import admin_bp
from routes.home import home_bp
from routes.user import user_bp
from routes.event import event_bp

def register_routes(app: Flask):
    app.register_blueprint(admin_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(event_bp)