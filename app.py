from flask import Flask, render_template, Markup, make_response, request,\
    redirect, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
import json
import requests
import models
import constants


#Config objects for SQLAlchemy
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
    user = request.cookies.get('adventoflove_username')
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

    # Markup converts from text to html
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
    # This code is given to us after making a post to github in order to
    # get the accessToken. With it, we can request for the information of
    # a certain user, but we only need the name and the email
    try:
        code = request.args.get('code')
        accessToken = getGithubAccessToken(code)
        username, email = getNameAndEmailFromGithub(accessToken)
        newUser = storeUserWithJson(username, email)
        app.logger.info('User created successfully: ' + str(newUser))
        response = make_response(url_for('index'))
        response.set_cookie('adventoflove_username', username)
        return response
    except Exception as e:
        app.logger.error(e)

    return redirect(url_for('index'))


def getGithubAccessToken(code):
    headers = {'Accept': 'application/json'}
    try:
        apiResponseFromGithub = json.loads(
            requests.post('https://github.com/login/oauth/access_token',
                          data={'client_id': constants.GITHUB_CLIENT_ID,
                                'client_secret': constants.GITHUB_CLIENT_SECRET,
                                'code': code},
                          headers=headers).content)

        return apiResponseFromGithub['access_token']
    except:
        raise Exception('Couldnt retrieve access token from github')


def getNameAndEmailFromGithub(accessToken):
    headers = {'Accept': 'application/json'}
    try:
        userInfo = json.loads(
            requests.get('https://api.github.com/user?' +
                         'access_token=' + accessToken,
                         headers=headers).content)
        return (userInfo['name'], userInfo['email'])
    except:
        raise Exception("Couldn't retrieve the user and email from api.github")


def storeUserWithJson(username, email):
    try:
        newUser = models.User(username, email)
        db.session.add(newUser)
        db.session.commit()
        return newUser
    except:
        db.session.rollback()
        raise Exception('Rollbacking the Database Session')


@app.route('/api/login/facebook', methods=['POST'])
def callbackLoginWithFacebook():
    try:
        username = request.form['name']
        email = request.form['email']
        newUser = storeUserWithJson(username, email)
        app.logger.info('new user created! ' + str(newUser))
        return '1'
    except Exception as e:
        app.logger.error(e)
        return '0'


@app.route('/logged')
def loggedIn():
    return make_response('False')


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
