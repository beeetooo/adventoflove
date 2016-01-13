from flask import Flask, render_template, Markup, make_response, request,\
    redirect, url_for, session, flash
# from flask.ext.sqlalchemy import SQLAlchemy
import json
import pymongo
import os
import requests
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'postgresql://postgres:kiensabe1@localhost/adventoflove'
# db = SQLAlchemy(app)
app.secret_key = "asdaisofasdfoinaidjfoadf"
# app.config["MONGODB_SETTINGS"] = {'DB': "adventoflove"}
# app.config["SECRET_KEY"] = "KeepThisS3cr3t"
# mongo = PyMongo(app)
# connection = pymongo.Connection()
# db = connection.adventoflove
# users = db.users
app.config.from_object(os.environ['APP_SETTINGS'])
loggedIn = False


@app.route('/')
def index():
    user = users.find()
    for i in user:
        print i
    return render_template('index.html', user=user)


@app.route('/day/<int:day>')
def getDay(day):
    if day <= 0 or day > 14:
        return 'Day is out of range: ' + day

    day = str(day)

    problem = [Markup(i.decode('utf8'))
               for i in open('static/input/' + day).readlines()]

    return render_template('day.html',
                           day=day,
                           problem=problem[1:],
                           name=problem[0])


@app.route('/day/<int:day>/input')
def getInput(day):
    if day <= 0 or day > 14:
        return 'Day is out of range: ' + day

    day = str(day)

    resp = make_response(''.join(open('static/input/input' + day).readlines()))
    resp.headers['Content-Type'] = 'text/plain'
    return resp


@app.route('/api/login/github')
def callbackLoginWithGithub():
    client_id = 'afe3fcfa67c8241657e1'
    client_secret = 'cd7fb231409e0c4ab10538fdf430a0f10a0ad162'
    code = request.args.get('code')
    headers = {'Accept': 'application/json'}
    apiReply = requests.post('https://github.com/login/oauth/access_token',
                             data={'client_id': client_id,
                                   'client_secret': client_secret,
                                   'code': code},
                             headers=headers)

    apiToken = json.loads(apiReply.content)
    response = make_response(apiToken['access_token'])
    response.headers['Content-Type'] = 'text/plain'
    return response


@app.route('/api/login/facebook', methods=['POST'])
def callbackLoginWithFacebook():
    app.loggedIn = True
    return request.form['name']


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logged')
def loggedIn():
    return make_response(app.LoggedIn)


@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


@app.route('/stats')
def stats():
    return render_template('stats.html')


@app.errorhandler(404)
def not_found(e):
    return 'Not found'


if __name__ == '__main__':
    app.run(debug=True)
