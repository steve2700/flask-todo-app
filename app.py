from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'taskbuddy27@gmail.com'
app.config['MAIL_PASSWORD'] = 'gogochuchu27'
app.config['MAIL_DEFAULT_SENDER'] = 'taskbuddy27@gmail.com'

db = SQLAlchemy(app)
mail = Mail(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)
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

            # Send email notification
            send_notification_email(new_task)

            return redirect('/')
        except Exception as e:
            return f'There was an issue adding your task: {str(e)}'
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
    except Exception as e:
        return f'There was a problem deleting that task: {str(e)}'


def send_notification_email(task):
    subject = 'New Task Added'
    recipient = 'user@example.com'  # Replace with the recipient's email address
    body = f'A new task has been added please dont forget to look out: {task.content}'

    with app.app_context():
        msg = Message(subject=subject, recipients=[recipient], body=body)
        mail.send(msg)


if __name__ == '__main__':
    app.run(debug=True)

