from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField, TextAreaField, Field
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
class PlainTextWidget(object):
    def __call__(self, field, **kwargs):
        return field.data if field.data else ''

class EntryForm(FlaskForm):
    entry_id = StringField('Entry ID')
    date = StringField('Date')
    posted_date = StringField('Posted Date')
    check_number = StringField('No.')
    name = StringField('Name')
    description = StringField('Description')
    debit = StringField('Debit')
    credit = StringField('Credit')
    amount = StringField('Amount')
    account_type = StringField('Account Type')
    tag_id = StringField('Category')
    submit = SubmitField('Upload')
    accountType = SelectField('Account Type')
    file = FileField()
    backup = SubmitField('Backup')
    restore = SubmitField('Restore')

class SummaryForm(FlaskForm):
    category = StringField()
    amount = StringField('Amount')

class AliasForm(FlaskForm):
    name = StringField() # entry name
    description = StringField('Description: ')
    exactMatch = BooleanField('Exact Match', default='checked')
    id = StringField('Entry ID')
    submit = SubmitField('Rename')
    cancel = SubmitField('Cancel')



class CategoryForm(FlaskForm):
    category = SelectField('Category')
    subCategory = SelectField('Sub-Category')
    name = StringField('Name')
    description = StringField('Description')
    id = StringField('Entry ID')
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')


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