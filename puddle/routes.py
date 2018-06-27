import os
import secrets
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from puddle import app, bcrypt, db
from puddle.forms import RegistrationForm, LoginForm, UpdateAccountInfoForm
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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Are you sure your username and password are correct? :(', 'error')
    app.logger.debug(form.errors)
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')  # , methods=['POST']
def logout():
    logout_user()
    return redirect(url_for('home'))


def set_profile_image(form_image):
    image_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_image.filename)
    image_name = image_hex + file_ext
    image_path = os.path.join(app.root_path, 'static/profile_images', image_name)
    form_image.save(image_path)
    return image_name


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountInfoForm()
    if form.validate_on_submit():
        if form.profile_image.data:
            image_file = set_profile_image(form.profile_image.data)
            current_user.profile_image = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_image = url_for('static', filename='profile_images/' + current_user.profile_image)
    return render_template('account.html', title='Account', profile_image=profile_image, form=form)