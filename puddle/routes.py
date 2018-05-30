from flask import render_template, url_for, flash, redirect
from puddle import app, bcrypt, db
from puddle.forms import RegistrationForm, LoginForm, user_check_dummy
from puddle.models import User, Post

posts = []

@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
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
