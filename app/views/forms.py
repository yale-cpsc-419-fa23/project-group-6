from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
# from wtforms.fields.html5 import DateField
from wtforms import DateField
from wtforms import StringField

from wtforms.validators import DataRequired, EqualTo, Optional, Email

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SettingsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional()])
    confirm_new_password = PasswordField(
        'Confirm New Password',
        validators=[
            EqualTo('new_password', message='Passwords must match.'),
            Optional()
        ]
    )
    submit = SubmitField('Update Settings')
