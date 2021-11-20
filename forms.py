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
    PasswordField
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


# Register form
class RegisterForm(FlaskForm):
    """
        Create contact form model
        Define field = WTF Fieldtype
            Set label
            Set any validators and messages
    """

    username = StringField(
        'Username',
        [
            InputRequired(),
            Length(min=3)
        ]
    )
    password = PasswordField(
        'Password',
        [
            InputRequired(),
            Length(min=8),
            EqualTo('confirm', message='Passwords must match')
        ]
    )
    confirm = PasswordField(
        'Confirm Password',
        [
            InputRequired()
        ]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Send')
