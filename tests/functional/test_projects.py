import json


def test_create_project(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/projects' page is requested (GET)
    THEN check the response is valid
    """
    from flaskr import db
    from flaskr.models import Project
    token = __get_auth_token__(app, test_client)
    response = test_client.post("/projects", json={
        "title": "title",
        "url": "url",
        "description": "description",
        "isPublic": "true",
        "company": "1",
        "technologies": "",
        "industries": "",
        "attachments": "",
    }, headers={"x-access-tokens": token})
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    print(response_data)
    assert response_data['id'] is not None
    with app.app_context():
        assert db.session.query(Project).count() == 1


def test_project_edit(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/projects/<id>' page is requested (POST)
    THEN check the response is valid
    """
    __insert_projects_to_db__(app)
    response = test_client.put("/projects/1", json={
        "title": "title",
        "url": "url",
        "description": "description",
        "is_public": "true",
    })
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert response_data['title'] == "title"
    assert response_data['url'] == "url"
    assert response_data['description'] == "description"
    assert response_data['is_public'] == True


def test_project_delete(test_client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/projects/<id>' page is requested (DELETE)
    THEN check the response is valid
    """
    from flaskr import db
    from flaskr.models import Project
    __insert_projects_to_db__(app)
    response = test_client.delete("/projects/1")
    assert response.status_code == 200
    with app.app_context():
        assert db.session.query(Project).count() == 3


def __get_auth_token__(app, test_client):
    from flaskr import db
    from flaskr.models import User

    with app.app_context():
        db.session.add(User(
            id=1,
            first_name="first_name",
            last_name="last_name",
            phone_number="phone_number",
            email="asd@asd.asd",
            password=User._generate_password_hash("asd")
        ))

        response = test_client.post("/login", data={"email": "asd@asd.asd", "password": "asd"})
        assert response.status_code == 200
        response_data = json.loads(response.data.decode("utf-8"))
        return response_data['token']


def __insert_projects_to_db__(app):
    from flaskr import db
    from flaskr.models import Project, Industry, Technology, Company

    mock_companies = [
        Company(id=1),
        Company(id=2),
        Company(id=3),
        Company(id=4),
    ]

    mock_industries = [
        Industry(id=1, name="asdad1"),
        Industry(id=2, name="asdad2"),
        Industry(id=3, name="asdad3"),
    ]
    mock_technologies = [
        Technology(id=1, name="asdad1"),
        Technology(id=2, name="asdad2"),
        Technology(id=3, name="asdad3"),
    ]

    mock_projects = [
        Project(id=0, title="Maxer", url="hort@gmail.com", description="111-111-111", is_public=True,
                technologies=[mock_technologies[0], mock_technologies[1]], industries=[mock_industries[0]],
                company_id=1),
        Project(id=1, title="Maxer1", url="hort@gmail.com", description="111-111-111", is_public=True,
                technologies=[mock_technologies[2], mock_technologies[1]],
                industries=[mock_industries[1], mock_industries[2]],
                company_id=2),
        Project(id=2, title="Maxer2", url="hort@gmail.com", description="111-111-111", is_public=True,
                technologies=[mock_technologies[0]],
                industries=[mock_industries[2], mock_industries[0]],
                company_id=3),
        Project(id=3, title="Maxer3", url="hort@gmail.com", description="111-111-111", is_public=True,
                technologies=[mock_technologies[1]],
                company_id=4),
    ]
    with app.app_context():
        db.session.add_all(mock_companies)
        db.session.add_all(mock_industries)
        db.session.add_all(mock_technologies)
        db.session.add_all(mock_projects)
        db.session.commit()
