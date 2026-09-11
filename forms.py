from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField,SubmitField
from wtforms.validators import DataRequired,Email,Length
class Registration(FlaskForm):
    name = StringField("Full Name",validators=[DataRequired()])
    password = PasswordField("Enter Password",validators=[DataRequired(),Length(min = 8)])
    email = StringField("Enter Gmail",validators=[DataRequired(),Email()])
    submit= SubmitField("Register")
    
