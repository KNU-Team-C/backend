import pytest
from _pytest import monkeypatch


@pytest.fixture(scope='module')
def new_user():
    mp = monkeypatch.MonkeyPatch()
    mp.setenv('DATABASE_URI', 'postgresql://postgres:max21042002@localhost/companies')
    mp.setenv('SECRET_KEY', 'Yduti0h363VCUfw2')
    from flaskr.models import User

    user = User(first_name="Maxer", last_name="Yudkin", email="hort@gmail.com", phone_number="111-111-111",
                password="111")
    return user


@pytest.fixture
def test_client():
    mp = monkeypatch.MonkeyPatch()
    mp.setenv('DATABASE_URI', 'postgresql://postgres:max21042002@localhost/companies')
    mp.setenv('SECRET_KEY', 'Yduti0h363VCUfw2')
    from flaskr import app

    test_client = app.test_client()
    yield test_client
