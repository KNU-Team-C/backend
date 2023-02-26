import os

from flask import Flask

from flaskr.model import user
from flaskr.database import db


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')

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
    from flaskr import hello

    app.register_blueprint(hello.bp)

    return app


app = create_app()
db.init_app(app)

with app.app_context():
    print('Creating database')
    db.create_all()
