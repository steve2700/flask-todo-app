from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from huey import RedisHuey
import redis

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a Redis client instance
redis_client = redis.Redis(host='localhost', port=6379)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False, unique=True)
    notes = db.Column(db.Text)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['task']
        task_category = request.form['category']
        new_task = Todo(content=task_content, category=task_category)
        try:
            db.session.add(new_task)
            db.session.commit()

            # Add the task content to Redis set for notifications
            redis_client.sadd('task_notifications', new_task.content)

            return redirect('/')
        except Exception as e:
            return f'There was an issue adding your task: {str(e)}'
    else:
        tasks = Todo.query.order_by(Todo.pub_date).all()

        # Get task notifications from Redis set
        task_notifications = redis_client.smembers('task_notifications')

        return render_template('index.html', tasks=tasks, notifications=task_notifications)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()

        # Remove the task content from Redis set for notifications
        redis_client.srem('task_notifications', task_to_delete.content)

        return redirect('/')
    except Exception as e:
        return f'There was a problem deleting that task: {str(e)}'

if __name__ == '__main__':
    huey = RedisHuey('flask_todo', host='localhost', port=6379)

    

