import flask_bcrypt
from rental import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=50), nullable=False)

    def __repr__(self):
        return f'User{self.id}'

    @property
    def password(self):
        return self.password    

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = flask_bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return flask_bcrypt.check_password_hash(self.password_hash, attempted_password)


class Tenant(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(length=50), nullable=False)
    phone_no = db.Column(db.String(length=50), nullable=False, unique=True)
    house_no = db.Column(db.String(length=50), nullable=False, unique=True)
    rent = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f'Tenant{self.id}'