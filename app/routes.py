from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Task
from . import db

bp = Blueprint('main', __name__)  # Создаем blueprint

@bp.route("/")
def index():
    status_filter = request.args.get('status', 'Все')
    if status_filter == 'Все':
        tasks = Task.query.filter(Task.status != 'Выполнена').all()
    else:
        tasks = Task.query.filter_by(status=status_filter).all()
    statuses = ['Все', 'Направлена в работу', 'В работе', 'Выполнена']
    return render_template("index.html", tasks=tasks, statuses=statuses, selected_status=status_filter)

@bp.route("/task/<int:task_id>")
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template("task_detail.html", task=task)

@bp.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        new_task = Task(title=title, description=description, status=status)
        db.session.add(new_task)
        db.session.commit()
        flash("Задача добавлена!")
        return redirect(url_for("main.index"))
    return render_template("task_form.html", task=None)

@bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == "POST":
        task.title = request.form['title']
        task.description = request.form['description']
        task.status = request.form['status']
        db.session.commit()
        flash("Задача обновлена!")
        return redirect(url_for("main.index"))
    return render_template("task_form.html", task=task)

@bp.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Задача удалена!")
    return redirect(url_for("main.index"))
