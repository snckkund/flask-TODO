"""
This is a Flask application for managing TODO tasks.
"""

from datetime import datetime, timezone
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class TODO(db.Model):
    """
    Represents a TODO task.
    """

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"{self.id} - {self.content}"

@app.route('/', methods=['GET','POST'])
def index():
    """
    Renders the index page and handles task creation.
    """
    if request.method == 'POST':
        todo = TODO(content=request.form['content'])

        try:
            db.session.add(todo)
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'There was an issue adding your task.'
    else:
        tasks = TODO.query.order_by(TODO.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    """
    Deletes a task with the given ID.
    """
    task_to_delete = TODO.query.get_or_404(task_id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception:
        return 'There was an issue deleting the task.'

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    """
    Updates a task with the given ID.
    """
    task = TODO.query.get_or_404(task_id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'There was an issue updating the task.'
    else:
        return render_template('update.html', task=task)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
