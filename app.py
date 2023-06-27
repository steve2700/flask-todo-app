from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from huey import RedisHuey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configure Redis for Huey task queue
huey = RedisHuey(url='redis://localhost:6379/0')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False, unique=True)
    notes = db.Column(db.Text)

    def __repr__(self):
        return '<Task %r>' % self.id


@huey.task()
def send_reminder(task_id):
    # Logic for sending reminder/notification
    task = Todo.query.get(task_id)
    if task:
        print(f"Sending reminder for task: {task.content}")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['task']
        task_category = request.form['category']
        new_task = Todo(content=task_content, category=task_category)
        try:
            db.session.add(new_task)
            db.session.commit()

            # Queue reminder task
            send_reminder(new_task.id)

            return redirect('/')
        except SQLAlchemyError as e:
            error_msg = str(e.__dict__.get('orig'))
            return f'There was an issue adding your task: {error_msg}'
    else:
        tasks = Todo.query.order_by(Todo.pub_date).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__.get('orig'))
        return f'There was a problem deleting that task: {error_msg}'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['task']
        task.notes = request.form['notes']  # Add this line to update the notes field
        try:
            db.session.commit()
            return redirect('/')
        except SQLAlchemyError as e:
            error_msg = str(e.__dict__.get('orig'))
            return f'There was an issue updating your task: {error_msg}'
    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)

