from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hellow World'

@app.route('/hellow')
def hello():
    return '<h1>Hello Flask</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)


@app.route('/user/<name>/<surname>')
def user(name, surname):
    return '<h1>Hello, {}{}!</h1>'.format(name, surname)


if __name__ == '__main__':
    app.run()

