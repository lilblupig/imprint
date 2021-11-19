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

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

mail.init_app(app)


@app.route("/")
@app.route("/get_locations")
def get_locations():
    """ Define test function """
    locations = mongo.db.locations.find()
    return render_template("index.html", locations=locations)

# Mail sending works with email hard coded into recipient - not working with environment variable - to address later
@app.route("/contact", methods=["GET", "POST"])
def contact():
    """ Contact form """
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('contact.html', form=form)
        else:
            msg = Message("Imprint contact message", sender="MAIL_USERNAME", recipients=["MAIL_USERNAME"])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.body.data)
            mail.send(msg)

            return 'Form posted.'
    elif request.method == 'GET':
        return render_template("contact.html", form=form)
