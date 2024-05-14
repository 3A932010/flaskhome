from flask import Flask, render_template, request
from flask import redirect, url_for
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

@app.route('/user/<username>',methods=['GET'])
def user(username):
    message = request.args.get('message')
    return render_template('user.html', name=username,message=message)

@app.route('/search', methods=['GET','POST'])
def search():
    global name
    username=name
    keyword = request.values['keyword']
    if keyword == '紅燈':
        message = '紅燈停!'
    elif keyword == '黃燈':
        message ='加速通過馬路或停下等候綠燈!'
    elif keyword == '綠燈':
        message ='綠燈行!'    
    else:
        message='請使用HTTP POST傳送資料'
    return render_template('user.html', name=username, message=message)

@app.route('/member/signin')
def signin():
    return render_template('member/signin.html')

@app.route('/member/login', methods=["POST"])
def login():
    if request.method == 'POST':
        username=request.form['username']
        userpassword=request.form['userpassword']
        message = '登入成功!'
        return redirect(url_for('user', username=username,message=message))
    else:
        render_template("member/signin.html")