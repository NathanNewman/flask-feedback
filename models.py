from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


class User(db.Model):
    """Users"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    feedback = db.relationship('Feedback', backref='user', cascade='all, delete-orphan')

    @classmethod
    def register_user(cls, form):
        username = form.username.data
        password = form.password.data
        password = User.encrypt(password)
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        return cls(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

    @staticmethod
    def encrypt(password):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        password = hashed_utf8
        return password

    @classmethod
    def authenticate(cls, form):
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


    @staticmethod
    def edit_user(form, userId):
        user = User.query.get(userId)
        user.username = form.username.data
        password = form.password.data
        user.password = User.encrypt(password)
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        db.session.commit()
        return userId

class Feedback(db.Model):
    """User feedback responses"""

    __tablename__= "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(140), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @classmethod
    def save_feedback(cls, userId, form):
        message = form.message.data
        return cls(message=message,user_id=userId)


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
