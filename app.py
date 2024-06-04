from flask import Flask, render_template, request
from flask import redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, SubmitField, validators
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import hashlib
import psycopg2
import psycopg2.extras
import dbconn
app = Flask(__name__, template_folder='templates',
            static_url_path='/static', static_folder='static')
app.secret_key='fd4723e200261a2271ea912571eaaa1d'
app.permanent_session_lifetime = timedelta(minutes=3)
app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql://{dbconn.user}:{dbconn.password}@{dbconn.host}/{dbconn.database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=false

#SQLAlchemy DB Connection
db_SQLAlchemy(app)

#DB Connection
def get_db_connection():
    conn=psycopg2.connect(
        host=dbconn.host,
        database=dbconn.database,
        user=dbconn.user,
        password=dbconn.password)
    return conn


#Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('帳號', [validators.DataRequired(),validators.Length(min=4, max=50)])
    userpass = PasswordField('密碼', [validators.DataRequired(),validators.Length(min=4, max=50),validators.EqualTo('confirm', message='密碼必須與確認密碼一樣')])
    confirm = PasswordField('確認密碼')
    name=StringField('姓名', [validators.DataRequired(), validators.Length(min=4, max=8)])
    birthday = DateField('生日', format='%Y-%m-%d')
    phone= StringField('電話', [validators.DataRequired(),validators.Length(min=7, max=13)])
    address = StringField('地址', [validators.Length(min=6, max=50)])
    email=StringField('電子郵件',[validators.DataRequired(), validators.Length(min=6, max=50)])
    submit = SubmitField('立即註冊')

#Member Class
class Member(db.Model):
    __table_name__='member'
    mid = db.Column(db.String(5), primary_key=True)
    name = db.Cloumn(db.String(8), unique=True,nullable=False)
    birthday = db.Column(db.Date)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(50), nullable=false)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    accounts= db.relationship('Account', backref='member', uselist=False)

    def __repr__(self):
        return f'<Member {self.username}>'

#Account Class
class Account(db.Model):
    __table_name__ = 'account'
    aid = db.Column(db.Integer,Primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    userpass = db.Column(db.String(50), nullable=False)
    mid = db.Column(db.String(5), db.ForeignKey('member.mid'))    

    def __repr__(self):
        return f'<Account {self.username}>'

#Role Class
class Role(db.Model):
    __table_name__ = 'role'
    id = db.Column(db.Integer,Primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    members=db.relationship('Member', backref='role')    

    def __repr__(self):
        return f'<Role {self.name}>'


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    db.create_all()
    return render_template('index.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

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

@app.route('/member/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        username=request.form['username']
        userpass=request.form['userpassword']
        md=hashlib.md5()
        md.update(userpass.encode('utf-8'))
        hashpass=md.hexdigest()

        '''conn=get_db_connection()
        cursor=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        SQL=f"SELECT username,userpass FROM account WHERE username='{username}';"
        cursor.execute(SQL)
        user=cursor.fetchone()
        cursor.close()
        conn.close()'''

        user=Account.query.filter_by(username=username).first()
        if not user:
            return redirect(url_for('signin'))

        #if(username==user['username'] and hashpass == user[userpass]):
        if(username==user.username and hashpass == user.userpass):
            session.permanent = True
            session['username']=username
            return redirect(url_for('user'))
        else:
            return redirect(url_for('signin'))       
    else:
        if 'username' in session:
            return redirect(url_for('user'))
        
    return render_template("member/signin.html")

@app.route('/member/signup')
def signup():
    regform=RegistrationForm()
    return render_template('member/signup.html', form=regform)

@app.route('/member/join', methods=["POST"])
def join():
    if request.method == 'POST':
        regform = RegistrationForm()
        if regform.validate_on_submit():
            username = regform.username.data
            userpass = regform.userpass.data
            name = regform.name.data
            birthday = regform.birthday.data
            phone = regform.phone.data
            address= regform.address.data
            email= regform.email.data

            conn=get_db_connection()
            cursor = conn.cursor()

            SQL="SELECT COUNT(*) FROM member"
            cursor.execute(SQL)
            count = cursor.fetchone()[0]
            mid = 'm' + str(count + 1).zfill(4)

            SQL2 = f"INSERT INTO member VALUES('{mid}','{name}','{birthday}','{phone}','{address}','{email}');"
            cursor.execute(SQL2)

            SQL3 = f"INSERT INTO account(mid,username,userpass) VALUES('{mid}','{username}','{userpass}');"
            cursor.execute(SQL3)

            conn.commit()
            cursor.close()
            conn.close()

        return redirect(url_for('signin'))

@app.route('/member/forgot')
def forgot():
    return 'Pass'

@app.route('/member/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('signin'))
     