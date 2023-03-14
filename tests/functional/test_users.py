
def test_login_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (POST)
    THEN check the response is valid
    """

    data = {
        "email": "hort@gmail.com",
        "password": "mypass",
    }
    response = test_client.post("/login", data=data)
    assert response.status_code == 200
    assert b'hort@gmail.com' in response.data
    assert b'password' not in response.data
    assert b'id' in response.data
    assert b'first_name' in response.data
    assert b'last_name' in response.data
    assert b'phone_number' in response.data
    assert b'token' in response.data


def test_login_get(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response a '405' status code is returning!
    """

    response = test_client.get("/login")
    assert response.status_code == 405
    assert b'token' not in response.data


def test_signup_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup' page is requested (POST)
    THEN check the response is valid
    """

    data = {
        "first_name": "Max",
        "last_name": "Yudkin",
        "email": "hort3@gmail.com",
        "phone_number": "111-11-111",
        "password": "mypass",
    }

    response = test_client.post("/signup", data=data)
    assert response.status_code == 200
    assert b'email' in response.data
    assert b'password' not in response.data
    assert b'id' in response.data
    assert b'first_name' in response.data
    assert b'last_name' in response.data
    assert b'phone_number' in response.data
    assert b'token' in response.data


def test_signup_get(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup' page is requested (GET)
    THEN check the response is valid
    """

    response = test_client.get("/signup")
    assert response.status_code == 405
    assert b'token' not in response.data

