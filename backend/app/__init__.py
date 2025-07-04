from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'supersecretkey'
    app.permanent_session_lifetime = timedelta(minutes=30)

    db.init_app(app)

    with app.app_context():
        from .models import User, Flashcard
        from .init_db import init_db
        init_db()

    return app
