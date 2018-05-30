from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, user_check_dummy
from incog import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///puddle.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_image}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.timestamp}')"

posts = []

# Flask views

@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'The tide awaits, {form.username.data} :)', 'success')
        return redirect(url_for('home'))
    app.logger.debug(form.errors)
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if user_check_dummy(form):
            flash(f'The tide awaits, {form.username.data} :)',
                  'success')  # Need to also ensure that an actual user has logged in
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Are you sure you used the right username and password?', 'error')
    app.logger.debug(form.errors)
    return render_template('login.html', title='Login', form=form)
