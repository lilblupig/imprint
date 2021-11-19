import os
from app import app, mongo
from flask import (
    flash,
    render_template,
    redirect,
    request,
    session,
    url_for
)

from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message, Mail

from forms import *

mail = Mail()

email_settings = {
    "MAIL_SERVER": os.environ.get("MAIL_SERVER"),
    "MAIL_PORT": os.environ.get("MAIL_PORT"),
    "MAIL_USE_SSL": os.environ.get("MAIL_USE_SSL"),
    "MAIL_USERNAME": os.environ.get("MAIL_USERNAME"),
    "MAIL_PASSWORD": os.environ.get("MAIL_PASSWORD"),
    "MAIL_DEFAULT_SENDER": os.environ.get("MAIL_DEFAULT_SENDER"),
    "ADMIN_EMAIL": os.environ.get("ADMIN_EMAIL")
}

app.config.update(email_settings)

mail.init_app(app)


@app.route("/")
@app.route("/get_locations")
def get_locations():
    """ Define test function """
    locations = mongo.db.locations.find()
    return render_template("index.html", locations=locations)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """ Contact form """
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == True:
            msg = Message("Imprint contact message", recipients=[email_settings["ADMIN_EMAIL"]])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.body.data)
            mail.send(msg)

            return 'Form posted.'
        else:
            return render_template('contact.html', form=form)

    elif request.method == 'GET':
        return render_template("contact.html", form=form)
