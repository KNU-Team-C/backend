import json


def test_all_users(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/users' page is requested (GET)
    THEN check the response is valid
    """
    __insert_users_to_db__(app)
    response = test_client.get("/admin/users")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert len(response_data["users"]) == 4


def test_banned_users(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/users?statuses=banned' page is requested (GET)
    THEN check the response is valid
    """
    __insert_users_to_db__(app)
    response = test_client.get("/admin/users?statuses=banned")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert len(response_data["users"]) == 2


def test_reported_users(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/users?statuses=reported' page is requested (GET)
    THEN check the response is valid
    """
    __insert_users_to_db__(app)
    response = test_client.get("/admin/users?statuses=reported")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert len(response_data["users"]) == 1


def test_total_users_amount(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/users_amount' page is requested (GET)
    THEN check the response is valid
    """
    __insert_users_to_db__(app)
    response = test_client.get("/admin/users_amount")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert response_data["amount"] == 4


def test_blocked_users_amount(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/users_amount?type=banned"' page is requested (GET)
    THEN check the response is valid
    """
    __insert_users_to_db__(app)
    response = test_client.get("/admin/users_amount?type=banned")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert response_data["amount"] == 2


def test_reported_users_amount(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/users_amount?type=reported' page is requested (GET)
    THEN check the response is valid
    """
    __insert_users_to_db__(app)
    response = test_client.get("/admin/users_amount?type=reported")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert response_data["amount"] == 1


def __insert_users_to_db__(app):
    from flaskr import db
    from flaskr.models import User, UserReport

    mock_reports = [
        UserReport(id=0, report_message="asdad", plaintiff_id=0, reported_user_id=1)
    ]
    mock_users = [
        User(id=0, first_name="Maxer", last_name="Yudkin", email="hort@gmail.com", phone_number="111-111-111",
             is_blocked=True, userReportsPlaintiff=[mock_reports[0]]),
        User(id=1, first_name="Maxer", last_name="Yudkin", email="hort1@gmail.com", phone_number="111-111-111",
             is_blocked=True, userReportsReported=[mock_reports[0]]),
        User(id=2, first_name="Maxer", last_name="Yudkin", email="hort2@gmail.com", phone_number="111-111-111",
             is_blocked=False),
        User(id=3, first_name="Maxer", last_name="Yudkin", email="hort3@gmail.com", phone_number="111-111-111",
             is_blocked=False),
    ]
    with app.app_context():
        db.session.add_all(mock_users)
        db.session.add_all(mock_users)
        db.session.commit()
