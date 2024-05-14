from flask import Flask, render_template, request
from flask import redirect, url_for
import hashlib
import psycopg2
import dbconn
app = Flask(__name__, template_folder='templates',
            static_url_path='/static', static_folder='static')
app.secret_key='fd4723e200261a2271ea912571eaaa1d'
name = ''

#DB Connection
def get_db_connection():
    conn=psycopg2.connect(
        host=dbconn.host,
        database=dbconn.database,
        user=dbconn.user,
        password=dbconn.password)
    return conn

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

@app.route('/user')
def user():
    if 'username' in seesion:
        username=session['username']
        return render_template('user.html', name=username)
    else:
        return redirect(url_for('signin'))
@app.route('/search', methods=['GET','POST'])
def search():
    if 'username' in session:
        username =session['username']
    
    if request.method =='POST':
        keyword = request.values['keyword']
        if keyword == '紅燈':
            message = '紅燈停!'
        elif keyword == '黃燈':
            message ='加速通過馬路或停下等候綠燈!'
        elif keyword == '綠燈':
            message ='綠燈行!'    
        else:
            message='請重新輸入!'
        return render_template('user.html', name=username, message=message)
    else:
        message='請使用HTTP POST傳送資料'
        return render_template('result.html', message=message)

@app.route('/member/signin')
def signin():
    return render_template('member/signin.html')

@app.route('/member/login', methods=["POST"])
def login():
    if request.method == 'POST':
        username=request.form['username']
        userpass=request.form['userpassword']
        md=hashlib.md5()
        md.update(userpass.encode('utf-8'))
        hashpass=md.hexdigest()

        conn=get_db_connection()
        cursor=conn.cursor()
        SQL=f"SELECT username,userpass FROM account WHERE username='{username}';"
        cursor.execute(SQL)
        user=cursor.fetchone()
        cursor.close()
        conn.close()

        if(username==user[0] and hashpass == user[1]):
            session['username']=username
            return redirect(url_for('user'))        
    else:
        if 'username' in session:
            return redirect(url_for('user'))
        render_template("member/signin.html")