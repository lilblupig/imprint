import os
from app import app
from flask_mail import Message, Mail


# Create instance of Flask-Mail Mail "class"
mail = Mail()

# Define settings for email sending in dictionary
email_settings = {
    "MAIL_SERVER": os.environ.get("MAIL_SERVER"),
    "MAIL_PORT": os.environ.get("MAIL_PORT"),
    "MAIL_USE_SSL": os.environ.get("MAIL_USE_SSL"),
    "MAIL_USERNAME": os.environ.get("MAIL_USERNAME"),
    "MAIL_PASSWORD": os.environ.get("MAIL_PASSWORD"),
    "MAIL_DEFAULT_SENDER": os.environ.get("MAIL_DEFAULT_SENDER"),
    "ADMIN_EMAIL": os.environ.get("ADMIN_EMAIL")
}

# Pull through mail settings
app.config.update(email_settings)

# Connect mail instance to Flask app
mail.init_app(app)

# Define mail function
def sendEmail(form_content):

    # Set mail subject and recipient
    msg = Message(
        "Imprint contact message",
        recipients=[email_settings["ADMIN_EMAIL"]]
    )

    # Set mail content
    msg.body = """
        From: %s <%s>
        %s
        """ % (form_content["name"], form_content["email"], form_content["body"])

    # Send mail
    mail.send(msg)
