"""Flask application factory for Task Management App."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name="development"):
    app = Flask(__name__)

    if config_name == "development":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskapp.db"
        app.config["SECRET_KEY"] = "dev-secret-key"
    elif config_name == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        app.config["SECRET_KEY"] = "test-secret-key"
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/taskapp"
        app.config["SECRET_KEY"] = "change-me-in-production"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from routes.auth import auth_bp
    from routes.tasks import tasks_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
