from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates',
            static_url_path='/static', static_folder='static')

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    name = request.args.get('name')
    return render_template('index.html', **locals())

@app.route('/shopping')
def shopping():
    return render_template('shopping.html')

@app.route('/ticket')
def ticket_saling():
    return render_template('ticket.html')

@app.route('/welfare')
def welfare_platform():
    return render_template('welfare.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)