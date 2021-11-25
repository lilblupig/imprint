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

            # Display success message for user
            return render_template('contact.html', success=True)

    return render_template("contact.html", form=form)


# Route for Registration form
@app.route("/register", methods=["GET", "POST"])
def register():
    """
        Register form:
        Define which model to use
        Check request type and either:
            GET = Load page
            POST = Validate, compare passwords and create document in DB
    """
    # Define model to use
    form = RegisterForm()

    if request.method == 'POST':

        # Check all fields are validated
        if form.validate() is True:

            # Check for existing username
            existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

            # If username is taken, ask user to choose a different name
            if existing_user:
                flash("Username taken, please choose again")
                return redirect(url_for("register"))

            # Create dictionary with user form data and obscure password
            register_user = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(request.form.get("password"))
            }

            # Add user document to DB
            mongo.db.users.insert_one(register_user)

            # Create session cookie for user
            session["user"] = request.form.get("username").lower()

            # Feedback success to user
            return render_template('register.html', success=True)

    return render_template("register.html", form=form)


# Route for login form
@app.route("/login", methods=["GET", "POST"])
def login():
    """
        Login form:
        Define which model to use
        Check request type and either:
            GET = Load page
            POST = Validate, compare form data to DB
    """
    # Define model to use
    form = LoginForm()

    if request.method == 'POST':

        # Check all fields are validated
        if form.validate() is True:

            # Check for existing username
            existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

            # If username entered does not exist, feedback to user
            if not existing_user:
                flash("Invalid username, please try again")
                return render_template('login.html', form=form)

            # If username does exist, check entered password against DB
            else:
                if check_password_hash(existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome back {}".format(request.form.get("username")))

            # If password does not match DB, feedback to user
                else:
                    flash("Invalid password, please try again")
                    return render_template('login.html', form=form)

            # Feedback success to user
            return render_template('login.html', success=True)

    return render_template('login.html', form=form)


# Route for logout
@app.route("/logout")
def logout():
    """
        Remove session cookie and feedback to user
    """
    # Delete user session
    flash("You have successfully been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Route for profile page
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
        Change password form:
        Define which model to use
        Check request type and either:
            GET = Load page
            POST = Validate, compare old password data to DB, check new passwords match and update DB
    """
    # Define model to use
    form = ChangePasswordForm()

    # Find user record from database
    user = mongo.db.users.find_one({"username": session["user"]})
    username = user["username"]

    # Check if a user is in session to try and avoid brute force access
    if session["user"]:
        if request.method == 'POST':

            # Check all fields are validated and new passwords match
            if form.validate() is True:

                # Check DB value matches that entered for old password in form
                if check_password_hash(user["password"], request.form.get("old_password")):

                    # Create variable containing hashed new password
                    update_password = generate_password_hash(request.form.get("new_password"))

                    # Update DB document with new password
                    mongo.db.users.update_one({"_id": user["_id"]}, {"$set": {"password": update_password}})

                    # Feedback success to user
                    return render_template('profile.html', username=username, success=True)

                flash("Incorrect existing password, please try again")

        return render_template("profile.html", username=username, form=form)

    return redirect(url_for("login"))


# Default route for gallery page
@app.route("/gallery")
def gallery():
    """ Get gallery page """
    return render_template("gallery.html")


# Default route for upload page
@app.route("/upload")
def upload():
    """ Get upload page """
    return render_template("upload.html")
