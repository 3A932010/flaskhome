from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates',
            static_url_path='/static', static_folder='static')
name = ''

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

@app.route('/user/<username>')
def user(username):
    global name
    name = username
    return render_template('user.html', name=username)

@app.route('/search', method=['POST'])
def search():
    global name
    username=name
    keyword = request.values['Keyword']
    if keyword == '紅燈':
        message = '紅燈停!'
    elif keyword == '黃燈':
        message ='綠燈行!'
    else:
        message='請重新輸入!'
    return render_template('user.html', name=username, message=message)