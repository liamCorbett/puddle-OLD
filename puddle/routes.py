from flask import render_template, url_for, flash, redirect
from flask_login import current_user, login_user, logout_user
from puddle import app, bcrypt, db
from puddle.forms import RegistrationForm, LoginForm
from puddle.models import User, Post

posts = []


@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'The tide awaits, {form.username.data} :)', 'success')
        return redirect(url_for('login'))
    app.logger.debug(form.errors)
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Are you sure your username and password are correct? :(', 'error')
    app.logger.debug(form.errors)
    return render_template('login.html', title='Login', form=form)


@app.route('/logout', methods=['POST'])
def login():
    logout_user()
    return redirect(url_for('home'))