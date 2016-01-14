from flask import Flask, render_template, Markup, make_response, request,\
    redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import json
import requests
import models


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///adventoflove'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)


@app.route('/')
def index():
    user = request.cookies.get('username')
    if not user:
        user = ""
    else:
        user = "back, " + user

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


@app.route('/api/login/facebook', methods=['GET'])
def callbackLoginWithFacebook():
    #Todo: Receive the user info and store into the db
    return redirect(url_for('index'))


@app.route('/logged')
def loggedIn():
    #Todo: Return if the user is logged in
    return make_response(False)


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
