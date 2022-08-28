from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, EmailField
#from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email


class SignInForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired("Username field is required!")])
    password = PasswordField('Password', validators=[InputRequired("Password field is required!")])
    submit = SubmitField('Sign In')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    message = TextAreaField('Message', validators=[InputRequired()], render_kw={'rows': 5})
    submit = SubmitField('Send')


class ForgotPass(FlaskForm):
    usersname = StringField('UsName', validators=[InputRequired()])
    realname = StringField('RealName', validators=[InputRequired()])
    oldpass = StringField('PassPass', validators=[InputRequired()])
    newpass = StringField('PassPass', validators=[InputRequired()])
    submit = SubmitField('Send')
