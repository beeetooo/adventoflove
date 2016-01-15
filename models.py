import app


class User(app.db.Model):
    __tablename__ = 'aoluser'

    id = app.db.Column(app.db.Integer, primary_key=True)
    username = app.db.Column(app.db.String(80))
    email = app.db.Column(app.db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Attempt(app.db.Model):
    __tablename__ = 'attempt'

    user_id = app.db.Column(app.db.Integer, primary_key=True)
    problem_number = app.db.Column(app.db.String(80))

    def __init__(self, user_id, problem_number):
        self.user_id = user_id
        self.problem_number = problem_number

    def __repr__(self):
        return '<Problem number: %r, User: >' % self.problem_number,
        self.user_id


class Problem(app.db.Model):
    __tablename__ = 'problem'

    id = app.db.Column(app.db.Integer, primary_key=True)
    problem_number = app.db.Column(app.db.String(80), unique=True)

    def __init__(self, problem_number):
        self.problem_number = problem_number

    def __repr__(self):
        return '<Problem number: %r>' % self.problem_number
