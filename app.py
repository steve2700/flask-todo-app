from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from flask_login import LoginManager, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '6f8673a8f3b9452dc5f08f8158f82db4'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.google.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'taskbuddy27@google.com'
app.config['MAIL_PASSWORD'] = 'gogochuchu27'
app.config['MAIL_DEFAULT_SENDER'] = 'taskbuddy27@google.com'

db = SQLAlchemy(app)
mail = Mail(app)

login_manager = LoginManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('todos', lazy=True))

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        task_content = request.form['task']
        new_task = Todo(content=task_content, user=current_user)
        try:
            db.session.add(new_task)
            db.session.commit()

            # Send email notification
            send_notification_email(new_task)

            return redirect('/')
        except Exception as e:
            return f'There was an issue adding your task: {str(e)}'
    else:
        tasks = Todo.query.filter_by(user=current_user).order_by(Todo.pub_date).all()
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please login.')
            return redirect('/login')

        new_user = User(email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please login.')
            return redirect('/login')
        except Exception as e:
            return f'There was an issue registering the user: {str(e)}'
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Invalid email or password.')
            return redirect('/login')

        # User authentication successful
        login_user(user)
        return redirect('/')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


def send_notification_email(task):
    subject = 'New Task Added'
    recipient = current_user.email
    body = f'A new task has been added: {task.content}'

    with app.app_context():
        msg = Message(subject=subject, recipients=[recipient], body=body)
        mail.send(msg)


if __name__ == '__main__':
    app.run(debug=True, port=8000)

