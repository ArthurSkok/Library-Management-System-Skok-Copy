from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length, Email
from flask import flash, session

def checkmember():
    if 'username' not in session:
        flash("Please login or signup to continue")
        member = 'No Member'

    elif session['username'] == 'Admin':
        member = 'Admin'

    else:
        member = 'Not Admin'

    return member

class UserPageForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6)])
    
class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6)])
    confirmpassword = PasswordField('confirmpassword', validators=[DataRequired(), Length(min=6)])
    email = EmailField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')

class SearchBookForm(FlaskForm):
    search = StringField('search', validators=[DataRequired(), Length(min=1)])

class AddBookForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=1)])
    authors = StringField('authors', validators=[DataRequired(), Length(min=1)])
    genre = StringField('genres', validators=[DataRequired(), Length(min=1)])
    availability = StringField('availability', validators=[DataRequired(), Length(min=1)])

class DeleteBookForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=1)])

class ReturnBookForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=1)])
    email = EmailField('email', validators=[DataRequired(), Email()])

class IssueBookForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=1)])
    email = EmailField('email', validators=[DataRequired(), Email()])

class AddMemberForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    username = StringField('username', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6)])

class DeleteMemberForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])

class IssueLateForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=1)])