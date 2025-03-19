import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from dotenv import load_dotenv  # Load environment variables

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Use environment variables instead of hardcoding secrets
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "fallback_secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///test.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

csrf = CSRFProtect(app)
db = SQLAlchemy(app)

# Todo Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Home Route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        if not task_content.strip():
            flash("Task cannot be empty!", "danger")
            return redirect(url_for("index"))

        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")
        except:
            flash("There was an issue adding your task", "danger")

        return redirect(url_for("index"))

    tasks = Todo.query.order_by(Todo.pub_date.desc()).all()
    return render_template("index.html", tasks=tasks)

# Delete Task
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash("Task deleted successfully!", "success")
    except:
        flash("There was an issue deleting the task", "danger")

    return redirect(url_for("index"))

# Update Task
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            flash("Task updated successfully!", "success")
        except:
            flash("There was an issue updating the task", "danger")

        return redirect(url_for("index"))

    return render_template("update.html", task=task)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
