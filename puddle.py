from flask import Flask, render_template, url_for
app = Flask(__name__)

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

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', puddles=puddles)