from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, user_check_dummy
from incog import SECRET_KEY
app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

puddles = [
    {
        'author': 'Liam Joseph Corbett',
        'title': 'Example puddle',
        'body': 'Hi, this is a puddle!',
        'timestamp': 'May 26, 2018'
    },
    {
        'author': 'Liam Joseph Corbett',
        'title': 'Example puddle 2',
        'body': 'Hi, this is another puddle!',
        'timestamp': 'May 26, 2018'
    }
]

@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html', puddles=puddles)


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
            flash(f'The tide awaits, {form.username.data} :)', 'success') #Need to also ensure that an actual user has logged in
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Are you sure you used the right username and password?', 'error')
    app.logger.debug(form.errors)
    return render_template('login.html', title='Login', form=form)