import pytest
from app import app, db, Todo

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200

def test_add_task(client):
    response = client.post("/", data={"content": "Test Task"})
    assert response.status_code == 302  # Redirect after adding task
    assert Todo.query.count() == 1

def test_update_task(client):
    with app.app_context():
        task = Todo(content="Old Task")
        db.session.add(task)
        db.session.commit()

    response = client.post(f"/update/{task.id}", data={"content": "Updated Task"})
    assert response.status_code == 302  # Redirect after update
    assert Todo.query.get(task.id).content == "Updated Task"

def test_delete_task(client):
    with app.app_context():
        task = Todo(content="Task to Delete")
        db.session.add(task)
        db.session.commit()

    response = client.get(f"/delete/{task.id}")
    assert response.status_code == 302  # Redirect after delete
    assert Todo.query.get(task.id) is None
