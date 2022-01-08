from rental.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, DataRequired


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=2), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Username', validators=[DataRequired()])    


class TenantsForm(FlaskForm):
    name = StringField(label='Name', validators=[Length(min=2), DataRequired()])
    phone_no = StringField(label='Phone No', validators=[Length(min=10, max=10), DataRequired()])
    house_no = StringField(label='House No', validators=[Email(), DataRequired()])
    rent = StringField(label='Rent', validators=[DataRequired()])   
    submit = SubmitField(label='Add')