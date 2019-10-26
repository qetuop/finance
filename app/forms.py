from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
#from app.models import User

'''
date = db.Column(db.DateTime)   # transaction for CC
    posted_date = db.Column(db.DateTime) # CC only
    check_number = db.Column(db.Integer) # checking/MM
    name = db.Column(db.String(120))  # user entered name
    description = db.Column(db.String(120))  # bank entered name
    debit = db.Column(db.Float)
    credit = db.Column(db.Float)
    '''
class EntryForm(FlaskForm):
    entry_id = StringField('Entry ID')
    date = StringField('Date')
    posted_date = StringField('Posted Date')
    check_number = StringField('No.')
    name = StringField('Name')
    description = StringField('Description')
    debit = StringField('Debit')
    credit = StringField('Credit')
    account_type = StringField('Account Type')
    category_id = StringField('Category')

class AliasForm(FlaskForm):
    name = StringField() # entry name
    id = StringField('Entry ID')
    submit = SubmitField('rename')
    cancel = SubmitField('cancel')

class CategoryForm(FlaskForm):
    category = StringField('Category')
    subCatagory = StringField('Sub-Category')
    name = StringField('Name')
    id = StringField('Entry ID')
    submit = SubmitField('rename')
    cancel = SubmitField('cancel')
'''
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
'''