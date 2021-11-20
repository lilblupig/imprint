"""
    Imprint Nov 2021
    Form models
"""

# Import dependencies
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    EmailField,
    TextAreaField,
    SubmitField,
    PasswordField,
)
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo
)

# Contact form
class ContactForm(FlaskForm):
    """
        Create contact form model
        Define field = WTF Fieldtype
            Set label
            Set any validators and messages
    """

    name = StringField(
        'Name',
        [
            InputRequired()
        ]
    )
    email = EmailField(
        'Email',
        [
            InputRequired(),
            Email(
                message=('Please enter a valid email address.')
            )
        ]
    )
    body = TextAreaField(
        'Query',
        [
            InputRequired(),
            Length(
                min=10,
                message=('Please write a message longer than 10 characters.')
            )
        ]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Send')


# Registration form
class RegisterForm(FlaskForm):
    """ Register for a user account """
    username = StringField(
        'Username',
        [InputRequired()]
    )
    password = PasswordField(
        'Password',
        [
            InputRequired(message="Please enter a password."),
        ]
    )
    confirmPassword = PasswordField(
        'Repeat Password',
        [
            EqualTo(password, message='Passwords must match.')
        ]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')