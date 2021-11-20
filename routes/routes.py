"""
    Imprint Nov 2021
    Routes for all pages
"""

# Import dependencies
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
from app import app, mongo
from forms import ContactForm, RegisterForm
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
    """
        Contact form:
        Define which model to use
        Check request type and either:
            GET = Load page
            POST = Validate, create message and send form
    """
    # Define model to use
    form = ContactForm()

    if request.method == 'POST':

        # Check all fields are validated
        if form.validate() is True:

            # Get form data and put in dictionary
            form_content = {
                "name": request.form.get("name"),
                "email": request.form.get("email"),
                "body": request.form.get("body")
            }

            # Call mail function and provide form data
            mail_config.send_email(form_content)

            return render_template('contact.html', success=True)

        # If fields not all validated reload form with messages
        else:
            return render_template('contact.html', form=form)

    elif request.method == 'GET':
        return render_template("contact.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
        Register form:
    """
    # Define model to use
    form = RegisterForm()

    if request.method == 'POST':

        # Check all fields are validated
        if form.validate() is True:
            # Check for existing username
            existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

            if existing_user:
                flash("Username already in use")
                return redirect(url_for("register"))

            register = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(request.form.get("password"))
            }

            mongo.db.users.insert_one(register)

            session["user"] = request.form.get("username").lower()

            flash("Registration successful")

            return render_template('register.html', success=True)

        # If fields not all validated reload form with messages
        else:
            return render_template('register.html', form=form)

    elif request.method == 'GET':
        return render_template("register.html", form=form)
