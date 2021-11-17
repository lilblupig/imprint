# Models

""" Import necessary data """
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo
)


class ContactForm(FlaskForm):
    """ Create contact form """
    name = StringField(
        'Name',
        [DataRequired()]
    )
    email = StringField(
        'Email',
        [
            Email(message=('Not a valid email address.')),
            DataRequired()
        ]
    )
    body = TextAreaField(
        'Query',
        [
            Length(min=4,
            message=('Your message is too short.')),
            DataRequired()
        ]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

