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
from forms import ContactForm, RegisterForm, LoginForm, ChangePasswordForm
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


# Route for Registration form
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

            register_user = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(request.form.get("password"))
            }

            mongo.db.users.insert_one(register_user)

            session["user"] = request.form.get("username").lower()

            flash("Registration successful")

            return render_template('register.html', success=True)

        # If fields not all validated reload form with messages
        else:
            return render_template('register.html', form=form)

    elif request.method == 'GET':
        return render_template("register.html", form=form)


# Route for login form
@app.route("/login", methods=["GET", "POST"])
def login():
    """
        Login form:
    """
    # Define model to use
    form = LoginForm()

    if request.method == 'POST':

        # Check all fields are validated
        if form.validate() is True:
            # Check for existing username
            existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

            if not existing_user:
                flash("Invalid username, please try again")
                return render_template('login.html', form=form)
            else:
                if check_password_hash(existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome back {}".format(request.form.get("username")))
                else:
                    flash("Invalid password, please try again")
                    return render_template('login.html', form=form)

            return render_template('login.html', success=True)

        # If fields not all validated reload form with messages
        else:
            return render_template('login.html', form=form)

    elif request.method == 'GET':
        return render_template('login.html', form=form)


# Route for profile page
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
        Change password form:
            Password updates, but then can't sign in*************************************************
    """
    # Define model to use
    form = ChangePasswordForm()

    # Find user record from database
    user = mongo.db.users.find_one({"username": session["user"]})

    if session["user"]:
        if request.method == 'POST':

            # Check all fields are validated
            if form.validate() is True:
                if check_password_hash(user["password"], request.form.get("old_password")):

                    update_password = {
                        "user": user["username"],
                        "password": generate_password_hash(request.form.get("new_password"))
                    }

                    mongo.db.users.update({"username": user["username"]}, update_password)

                    return render_template('profile.html', username=username, success=True)
                else:
                    flash("Incorrect existing password, please try again")
                    return render_template("profile.html", username=username, form=form)
            else:
                return render_template('profile.html', username=username, form=form)

        elif request.method == 'GET':
            username = user["username"]
            return render_template("profile.html", username=username, form=form)

    return redirect(url_for("login"))