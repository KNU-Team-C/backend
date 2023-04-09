import json


def test_all_requests_companies(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/requests_companies' page is requested (GET)
    THEN check the response is valid
    """
    __insert_data_to_db__(app)
    response = test_client.get("/admin/requests_companies")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert len(response_data["items"]) == 3


def test_verification_requests_companies(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/requests_companies?types=verification' page is requested (GET)
    THEN check the response is valid
    """
    __insert_data_to_db__(app)
    response = test_client.get("/admin/requests_companies?types=verification")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert len(response_data["items"]) == 2


def test_reported_requests_companies(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/requests_companies?types=reports' page is requested (GET)
    THEN check the response is valid
    """
    __insert_data_to_db__(app)
    response = test_client.get("/admin/requests_companies?types=reports")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert len(response_data["items"]) == 1

def test_all_requests_users(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/requests_users' page is requested (GET)
    THEN check the response is valid
    """
    __insert_data_to_db__(app)
    response = test_client.get("/admin/requests_users")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert len(response_data["items"]) == 1


def __insert_data_to_db__(app):
    from flaskr import db
    from flaskr.models import Company, CompanyReport, User, UserReport

    mock_reports = [
        CompanyReport(id=0, report_message="asdad", company_id=0, user_id=0)
    ]
    
    mock_companies = [
        Company(id=0, name="Maxer", email="hort@gmail.com", phone_number="111-111-111", is_verified=True,
                is_blocked=False, companyReports=[mock_reports[0]]),
        Company(id=1, name="Maxer1", email="hort1@gmail.com", phone_number="211-111-111", is_verified=True,
                is_blocked=False),
        Company(id=2, name="Maxer2", email="hort2@gmail.com", phone_number="311-111-111", is_verified=False,
                is_blocked=True),
        Company(id=3, name="Maxer3", email="hort3@gmail.com", phone_number="411-111-111", is_verified=False,
                is_blocked=True),
    ]

    mock_user_reports = [
        UserReport(id=0, report_message="asdad", plaintiff_id=0, reported_user_id=1)
    ]
    mock_users = [
        User(id=0, first_name="Maxer", last_name="Yudkin", email="hort@gmail.com", phone_number="111-111-111",
             is_blocked=True, userReportsPlaintiff=[mock_user_reports[0]]),
        User(id=1, first_name="Maxer", last_name="Yudkin", email="hort1@gmail.com", phone_number="111-111-111",
             is_blocked=True, userReportsReported=[mock_user_reports[0]]),
        User(id=2, first_name="Maxer", last_name="Yudkin", email="hort2@gmail.com", phone_number="111-111-111",
             is_blocked=False),
        User(id=3, first_name="Maxer", last_name="Yudkin", email="hort3@gmail.com", phone_number="111-111-111",
             is_blocked=False),
    ]
    with app.app_context():
        db.session.add_all(mock_companies)
        db.session.add_all(mock_reports)
        db.session.add_all(mock_users)
        db.session.add_all(mock_user_reports)
        db.session.commit()
