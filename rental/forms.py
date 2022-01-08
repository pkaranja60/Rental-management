from rental.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, DataRequired, ValidationError


class RegistrationForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email')

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