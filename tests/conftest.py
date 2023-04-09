import pytest
from _pytest import monkeypatch
from decouple import config


@pytest.fixture
def app():
    DATABASE_URI = "sqlite://"
    SECRET_KEY = "asdasd"
    mp = monkeypatch.MonkeyPatch()
    mp.setenv('DATABASE_URI', DATABASE_URI)
    mp.setenv('SECRET_KEY', SECRET_KEY)

    from flaskr import create_app, db
    test_config = {
        "DATABASE_URI": "sqlite://",
        "SECRET_KEY": "asdasd"
    }
    app = create_app(test_config)
    db.init_app(app)

    with app.app_context():
        print("Create database")
        db.create_all()

    yield app


@pytest.fixture
def new_user(app):
    from flaskr.models import User

    user = User(first_name="Maxer", last_name="Yudkin", email="hort@gmail.com", phone_number="111-111-111",
                password=User._generate_password_hash("111"))
    return user


@pytest.fixture
def test_client(app):
    return app.test_client()
