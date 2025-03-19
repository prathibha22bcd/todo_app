import pytest
from app import app, db, Todo

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Todo Webapp" in response.data

def test_add_task(client):
    response = client.post("/", data={"content": "Test Task"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Task" in response.data

def test_update_task(client):
    with app.app_context():
        task = Todo(content="Old Task")
        db.session.add(task)
        db.session.commit()
    response = client.post(f"/update/{task.id}", data={"content": "Updated Task"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Updated Task" in response.data

def test_delete_task(client):
    with app.app_context():
        task = Todo(content="Task to Delete")
        db.session.add(task)
        db.session.commit()
    response = client.get(f"/delete/{task.id}", follow_redirects=True)
    assert response.status_code == 200
    assert b"Task to Delete" not in response.data
