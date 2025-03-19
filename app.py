from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf.csrf import CSRFProtect  # Import CSRF protection

app = Flask(__name__)

# Enable CSRF protection
csrf = CSRFProtect(app)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key_here"  # Required for CSRF

db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Route to display tasks
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        if not task_content.strip():
            return redirect("/")
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding your task."

    tasks = Todo.query.order_by(Todo.pub_date.desc()).all()
    return render_template("index.html", tasks=tasks)

# Route to delete a task
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was an issue deleting your task."

# Route to update a task
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task."
    return render_template("update.html", task=task)

if __name__ == "__main__":
    db.create_all()  # Ensure database tables are created
    app.run(debug=True)
