from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, TextAreaField
from wtforms.validators import EqualTo, InputRequired, Length


class RegistrationForm(FlaskForm):
    """Form for creating a new user."""

    username = StringField("Username", validators=[InputRequired(), Length(
        min=2, max=20, message="Username must be 2 to 20 characters!")])
    password = PasswordField("Password", validators=[InputRequired(),
                                                     Length(
                                                         min=8, max=20, message="Password must be between 8 and 20 characters"),
                                                     EqualTo('confirm', message="Passwords must match!")])
    confirm = PasswordField("Re-enter Password")
    email = EmailField("Email", validators=[InputRequired(), Length(
        max=50, message="Email cannot be more than 50 characters!")])
    first_name = StringField("First Name", validators=[InputRequired(), Length(
        min=1, max=30, message="First Name cannot be more than 30 characters!")])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(
        min=1, max=30, message="Last Name cannot be more than 30 characters!")])


class LoginForm(FlaskForm):
    """Form to allow users to login in."""

    username = StringField("Username", validators=[InputRequired(), Length(
        min=2, max=20, message="Username must be 2 to 20 characters!")])
    password = PasswordField("Password", validators=[InputRequired(), Length(
        min=8, max=20, message="Password must be between 8 and 20 characters")])


class FeedbackForm(FlaskForm):
    """Form to allow users to post feeback."""

    message = TextAreaField("Message", validators=[InputRequired(), Length(max=140, message="Feedback message cannot be longer than 140 characters")])
