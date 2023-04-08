import json


def test_all_companies(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/companies' page is requested (GET)
    THEN check the response is valid
    """
    __insert_companies_to_db__(app)
    response = test_client.get("/admin/companies")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert len(response_data["companies"]) == 4


def test_banned_companies(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/companies?statuses=banned' page is requested (GET)
    THEN check the response is valid
    """
    __insert_companies_to_db__(app)
    response = test_client.get("/admin/companies?statuses=banned")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert len(response_data["companies"]) == 2


def test_reported_companies(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/companies?statuses=reported' page is requested (GET)
    THEN check the response is valid
    """
    __insert_companies_to_db__(app)
    response = test_client.get("/admin/companies?statuses=reported")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert len(response_data["companies"]) == 1

def __insert_companies_to_db__(app):
    from flaskr import db
    from flaskr.models import Company, CompanyReport

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
    with app.app_context():
        db.session.add_all(mock_companies)
        db.session.add_all(mock_reports)
        db.session.commit()
