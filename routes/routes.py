# Import dependencies
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
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message, Mail

# Import Object ID info from MongoDB
from bson.objectid import ObjectId

# Import local Forms code
from forms import *
from config import mail_config


# Default route for homepage
@app.route("/")
@app.route("/get_locations")
def get_locations():
    """ Define test function """
    locations = mongo.db.locations.find()
    return render_template("index.html", locations=locations)


# Route for Contact Form
@app.route("/contact", methods=["GET", "POST"])
def contact():
    """ Contact form """
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == True:
            form_content = {
                "name": request.form.get("name"),
                "email": request.form.get("email"),
                "body": request.form.get("body")
            }

            mail_config.sendEmail(form_content)

            return 'Form posted.'
        else:
            return render_template('contact.html', form=form)

    elif request.method == 'GET':
        return render_template("contact.html", form=form)
