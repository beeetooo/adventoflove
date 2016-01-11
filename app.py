from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/day/<int:day>')
def getDay(day):
    if day < 0 or day > 14:
        return 'Day is out of range: ' + day

    if day < 10:
        day = '0' + str(day)

    problem = [i.decode('utf8')
               for i in open('static/input/' + day).readlines()]

    return render_template('day.html',
                           day=day,
                           problem=problem[1:],
                           name=problem[0])


@app.errorhandler(404)
def not_found(e):
    return 'Not found'


if __name__ == '__main__':
    app.run(debug=True)