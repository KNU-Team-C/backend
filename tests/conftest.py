import pytest
from _pytest import monkeypatch
from decouple import config


@pytest.fixture(scope='module')
def new_user():
    DATABASE_URI = config('DATABASE_URI')
    SECRET_KEY = config('SECRET_KEY')
    mp = monkeypatch.MonkeyPatch()
    mp.setenv('DATABASE_URI', DATABASE_URI)
    mp.setenv('SECRET_KEY', SECRET_KEY)
    from flaskr.models import User

    user = User(first_name="Maxer", last_name="Yudkin", email="hort@gmail.com", phone_number="111-111-111",
                password="111")
    return user


@pytest.fixture
def test_client():
    DATABASE_URI = config('DATABASE_URI')
    SECRET_KEY = config('SECRET_KEY')
    mp = monkeypatch.MonkeyPatch()
    mp.setenv('DATABASE_URI', DATABASE_URI)
    mp.setenv('SECRET_KEY', SECRET_KEY)
    from flaskr import app

    test_client = app.test_client()
    yield test_client
