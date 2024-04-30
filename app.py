from flask import Flask, render_template

app = Flask(__name__, template_folder='templates',
            static_url_path='/static', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shopping')
def shopping():
    return render_template('shopping.html')

@app.route('/ticket')
def ticket_saling():
    return render_template('ticket_saling.html')

@app.route('/welfare')
def welfare_platform():
    return render_template('welfare_platform.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)