from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Members(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(40))
    email = db.Column(db.String(40), unique=True)
    cost = db.Column(db.FLOAT)

    def __init__(self,username,password, email, cost):
        self.username = username
        self.password = password
        self.email = email
        self.cost = cost

class Borrows(db.Model):
    __tablename__ ='borrows'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    email = db.Column(db.String(40))
    issuedt = db.Column(db.Date)
    late = db.Column(db.Integer)
    fine = db.Column(db.FLOAT)

    def __init__(self, title, email, issuedt, late, fine):
        self.title = title
        self.email = email
        self.issuedt = issuedt
        self.late = late
        self.fine = fine

class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    authors = db.Column(db.String(40))
    genre = db.Column(db.String(40))
    availability = db.Column(db.String(40))

    def __init__(self,title,authors,genre,availability):
        self.title = title
        self.authors = authors
        self.genre = genre
        self.availability = availability