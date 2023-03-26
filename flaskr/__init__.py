import os

from flask import Flask
from flask_cors import CORS

from flaskr import models
from flaskr.database import db
from flaskr.models import User, UserReport, Technology, Industry, Project, Company


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # apply the blueprints to the app
    from flaskr import hello, auth, admin_users, admin_companies, admin_requests, company_edit

    app.register_blueprint(hello.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin_users.bp)
    app.register_blueprint(admin_companies.bp)
    app.register_blueprint(admin_requests.bp)
    app.register_blueprint(company_edit.bp)

    return app


app = create_app()
db.init_app(app)
CORS(app)

with app.app_context():
    print('Creating database')
    db.create_all()
