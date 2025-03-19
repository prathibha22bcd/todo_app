import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Use environment variables for security
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
        task_content = request.form.get("content", "").strip()

        if not task_content:
            flash("Task cannot be empty!", "danger")
            return redirect(url_for("index"))

        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding task: {str(e)}", "danger")

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
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting task: {str(e)}", "danger")

    return redirect(url_for("index"))

# Update Task
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        new_content = request.form.get("content", "").strip()

        if not new_content:
            flash("Task cannot be empty!", "danger")
            return redirect(url_for("update", id=id))

        task.content = new_content
        try:
            db.session.commit()
            flash("Task updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating task: {str(e)}", "danger")

        return redirect(url_for("index"))

    return render_template("update.html", task=task)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

