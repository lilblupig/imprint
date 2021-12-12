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

# Import dependencies for Cloudinary
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Get Cloudinary account data
cloudinary.config(
  cloud_name=os.environ.get("CLOUD_NAME"),
  api_key=os.environ.get("API_KEY"),
  api_secret=os.environ.get("API_SECRET")
)

# Import Object ID info from MongoDB
from bson.objectid import ObjectId

# Import local Forms code
from app import app, mongo
from forms import ContactForm, RegisterForm, LoginForm, ChangePasswordForm, DeleteProfileForm, UploadImageForm, EditImageForm
from config import cloudinary_config, mail_config


# Default route for homepage
@app.route("/")
@app.route("/gallery")
def gallery():
    """ Get gallery page """

    # Get all locations for filter box
    locations = mongo.db.locations.find()

    # Get images from database
    images = mongo.db.images.find().sort("_id", -1)

    return render_template("gallery.html", images=images, locations=locations)


# Route for gallery free text search
@app.route("/image_search", methods=["GET", "POST"])
def image_search():
    """ Collect info from search input and use DB index to return results """

    # Get search form data
    image_search = request.form.get("image_search")

    # Search database using permanent text index
    images = mongo.db.images.find({"$text": {"$search": image_search}})

    # If DB search yields no results, flash user message
    if mongo.db.images.count_documents({"$text": {"$search": image_search}}) < 1:
        flash("No results found")

    # Get all locations for filter box
    locations = mongo.db.locations.find()

    return render_template("gallery.html", images=images, locations=locations)


# Route for gallery dropdown filter
@app.route("/location_filter", methods=["GET", "POST"])
def location_filter():
    """ Collect info from dropdown and query DB for results """

    # Get search form data
    location_choice = request.form.get("location_filter")

    # Search database using permanent text index
    images = mongo.db.images.find({"location": location_choice})

    # If DB search yields no results, flash user message
    if mongo.db.images.count_documents({"location": location_choice}) < 1:
        flash(location_choice)

    # Get all locations for filter box
    locations = mongo.db.locations.find()

    return render_template("gallery.html", images=images, locations=locations)


# Route for displaying Single Image
@app.route("/single_image/<image_id>")
def single_image(image_id):
    """ Get single image and info """

    # Get image document id
    image = mongo.db.images.find_one({"_id": ObjectId(image_id)})

    return render_template("single_image.html", image=image)


# Route for About page
@app.route("/about")
def about():
    """ Get about page """
    return render_template("about.html")


# Route for Contact Form
@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
        Contact form:
        Define which form to use
        Check request type and either:
            GET = Load page
            POST = Validate, create message and send form
    """
    # Define form to use
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

            flash("Thank you for your message, we will be in touch as soon as we can.")

            # Display success message for user
            return redirect(url_for("gallery"))

    return render_template("contact.html", form=form)


# Route for Registration form
@app.route("/register", methods=["GET", "POST"])
def register():
    """
        Register form:
        Define which form to use
        Check request type and either:
            GET = Load page
            POST = Validate, compare passwords and create document in DB
    """
    # Define form to use
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
                "password": generate_password_hash(request.form.get("password")),
                "is_admin": "false"
            }

            # Add user document to DB
            mongo.db.users.insert_one(register_user)

            # Create session cookie for user
            session["user"] = request.form.get("username").lower()
            session["admin"] = "false"

            # Feedback success to user and direct to About page
            flash("Welcome {}, thank you for registering!".format(register_user["username"]))
            return redirect(url_for("about"))

    return render_template("register.html", form=form)


# Route for login form
@app.route("/login", methods=["GET", "POST"])
def login():
    """
        Login form:
        Define which form to use
        Check request type and either:
            GET = Load page
            POST = Validate, compare form data to DB
    """
    # Define form to use
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
                    session["admin"] = existing_user["is_admin"].lower()
                    flash("Welcome back {}".format(request.form.get("username")))
                    if session["admin"] == "true":
                        flash("You are signed in as an Administrator")

            # If password does not match DB, feedback to user
                else:
                    flash("Invalid password, please try again")
                    return render_template('login.html', form=form)

            # Feedback success to user on home page
            return redirect(url_for("gallery"))

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
        Define which form to use
        Check request type and either:
            GET = Load page
            POST = Validate, compare old password data to DB, check new passwords match and update DB
    """
    # Define form to use
    form = ChangePasswordForm()

    # Find user record from database
    user = mongo.db.users.find_one({"username": session["user"]})
    username = user["username"]

    # Find posts made by user
    images = mongo.db.images.find({"owner": username})

    # Check if a the user in session owns the profile to try and avoid brute force access
    if session["user"] == user["username"]:
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

        return render_template("profile.html", images=images, username=username, form=form)

    # If user does not match session user, log them out and inform them why
    flash("You are not authorised to view this page and have been logged out")
    session.pop("user")

    return redirect(url_for("login"))


# Route to delete profile
@app.route("/delete_profile", methods=["GET", "POST"])
def delete_profile():
    """ Get user information, delete posts, and profile """

    # Define form to use
    form = DeleteProfileForm()

    # Get locations and images for home page after deletion
    locations = mongo.db.locations.find()
    images = mongo.db.images.find()

    # Find user record from database
    user = mongo.db.users.find_one({"username": session["user"]})
    username = user["username"]

    # Find posts made by user
    posts = mongo.db.images.find({"owner": username})

    # Check if a user is in session to try and avoid brute force access
    if session["user"]:
        if request.method == 'POST':

            # Check all fields are validated and new passwords match
            if form.validate() is True:

                # Check DB value matches that entered for old password in form
                if check_password_hash(user["password"], request.form.get("old_password")):
                    # Delete posts
                    for post in posts:
                        # Remove images from Cloudinary and clear Cloudinary cache
                        cloudinary.uploader.destroy(post["cloudinary_id"], invalidate=True)
                        # Remove documents from DB
                        mongo.db.images.remove({"_id": post["_id"]})

                    # Remove session cookie
                    session.pop("user")

                    # Delete profile
                    mongo.db.users.remove({"_id": user["_id"]})

                    return redirect(url_for("gallery"))

                flash("Incorrect existing password, please try again")

    return render_template("delete_profile.html", form=form)


# Route for upload page
@app.route("/upload", methods=["GET", "POST"])
def upload():
    """ Get upload page """

    # Define form to use
    form = UploadImageForm()

    # Get location options and populate choices in upload form
    all_locations = mongo.db.locations.distinct('location_name')
    form.location.choices = [location for location in all_locations]

    # Find user record from database
    user = mongo.db.users.find_one({"username": session["user"]})
    username = user["username"]

    # Check if a user is in session to try and avoid brute force access
    if session["user"]:
        if request.method == 'POST':

            # Check all fields are validated and new passwords match
            if form.validate() is True:

                # Send image to Cloudinary account
                photo = request.files['photo']
                photo_upload = cloudinary.uploader.unsigned_upload(photo, "p6tbiahk")
                uploaded = {
                    "location": request.form.get("location"),
                    "decade": request.form.get("decade"),
                    "details": request.form.get("details"),
                    "tags": request.form.get("tags"),
                    "photo": photo_upload["secure_url"],
                    "cloudinary_id": photo_upload["public_id"],
                    "owner": username
                }

                # Add image document to DB
                mongo.db.images.insert_one(uploaded)

                return render_template('upload.html', success=True)

        return render_template("upload.html", form=form)

    # If no user is logged in, try to remove cookie as precaution and return user to login screen
    flash("You are not authorised to view this page and have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Route to edit a post
@app.route("/edit_image/<image_id>", methods=["GET", "POST"])
def edit_image(image_id):
    """ Get edit post page """

    # Get image document id and make locations available
    image = mongo.db.images.find_one({"_id": ObjectId(image_id)})
    locations = mongo.db.locations.find()

    # Define form to use
    form = EditImageForm(location=image["location"], decade=image["decade"], details=image["details"], tags=image["tags"])

    # Get location options and populate choices/defaults in edit form
    all_locations = mongo.db.locations.distinct('location_name')
    form.location.choices = [location for location in all_locations]

    # Find user record from database
    user = mongo.db.users.find_one({"username": session["user"]})

    # Check if a user is in session to try and avoid brute force access
    if session["user"] == image["owner"] or session["admin"] == "true":
        if request.method == 'POST':

            # Check all fields are validated and new passwords match
            if form.validate() is True:

                updated = {
                    "location": request.form.get("location"),
                    "decade": request.form.get("decade"),
                    "details": request.form.get("details"),
                    "tags": request.form.get("tags"),
                    "photo": image["photo"],
                    "cloudinary_id": image["cloudinary_id"],
                    "owner": image["owner"]
                }
                # Update document in DB
                mongo.db.images.update({"_id": image["_id"]}, updated)

                flash("Post updated succesfully!")

                return render_template('edit_image.html', image=image, success=True)

        return render_template("edit_image.html", image=image, form=form)

    # If logged in user is not admin or does not match the image owner, log out and explain
    flash("You are not authorised to edit this post and have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Route to delete a post
@app.route("/delete_image/<image_id>")
def delete_image(image_id):
    """ Delete a post """

    # Find user record from database
    user = mongo.db.users.find_one({"username": session["user"]})
    username = user["username"]

    # Get image from database
    image = mongo.db.images.find_one({"_id": ObjectId(image_id)})

    # Check if a user is in session to try and avoid brute force access
    if session["user"] == image["owner"] or session["admin"] == "true":

        # Remove document from DB
        mongo.db.images.remove({"_id": image["_id"]})

        # Remove image from Cloudinary
        cloudinary.uploader.destroy(image["cloudinary_id"])

        # Find posts made by user and define form for loading profile page
        images = mongo.db.images.find({"owner": username})
        form = ChangePasswordForm()

        flash("Post succesfully deleted")

        return render_template("profile.html", images=images, username=username, form=form)

    # If logged in user is not admin or does not match the image owner, log out and explain
    flash("You are not authorised to edit this post and have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Route for Admin User Management page
@app.route("/manage_users")
def manage_users():
    """
        Load all users for moderation
    """

    # Find user record from database
    user = mongo.db.users.find_one({"username": session["user"]})

    if session["admin"] == "true":

        # Find all users and display in alphabetical order
        users = mongo.db.users.find().sort("username", 1)

        return render_template("manage_users.html", users=users)

    flash("You are not authorised to view this page and have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Route for Admin toggle
@app.route("/admin_toggle/<user_toggle_id>")
def admin_toggle(user_toggle_id):
    """
        Toggle on or off admin permissions
    """

    # Find user record from database
    user = mongo.db.users.find_one({"username": session["user"]})

    # Check current logged in user has admin rights
    if session["admin"].lower() == "true":

        # Find user to be toggled
        user_toggle = mongo.db.users.find_one({"_id": ObjectId(user_toggle_id)})

        # Check current admin status
        if user_toggle["is_admin"].lower() == "false":
            # Toggle admin rights on
            mongo.db.users.update_one({"_id": user_toggle["_id"]}, {"$set": {"is_admin": "true"}})
        else:
            # Toggle admin rights off
            mongo.db.users.update_one({"_id": user_toggle["_id"]}, {"$set": {"is_admin": "false"}})

        flash("User updated succesfully!")

        return redirect(url_for("manage_users"))

    flash("You are not authorised to view this page and have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Route for admin to delete user profile
@app.route("/admin_delete_profile/<delete_user>", methods=["GET", "POST"])
def admin_delete_profile(delete_user):
    """ Get user information, delete posts, and profile """

    # Define form to use
    form = DeleteProfileForm()

    # Find admin user record from database
    user = mongo.db.users.find_one({"username": session["user"]})

    # Find user record from database
    deleting_user = mongo.db.users.find_one({"_id": ObjectId(delete_user)})
    deleting_username = deleting_user["username"]

    # Find posts made by user
    posts = mongo.db.images.find({"owner": deleting_username})

    # Check if a user is in session to try and avoid brute force access
    if session["admin"].lower() == "true":
        if request.method == 'POST':

            # Check all fields are validated and passwords match
            if form.validate() is True:

                # Check admin DB value matches that entered for old password in form
                if check_password_hash(user["password"], request.form.get("old_password")):
                    # Delete posts
                    for post in posts:
                        # Remove images from Cloudinary and clear Cloudinary cache
                        cloudinary.uploader.destroy(post["cloudinary_id"], invalidate=True)
                        # Remove documents from DB
                        mongo.db.images.remove({"_id": post["_id"]})

                    # Delete profile
                    mongo.db.users.remove({"_id": deleting_user["_id"]})

                    flash("User deleted succesfully!")

                    return redirect(url_for("manage_users"))

            flash("Incorrect password, please try again")

    return render_template("admin_delete_profile.html", form=form, deleting_user=deleting_user)


# Route for Admin Image Management page
@app.route("/manage_images")
def manage_images():
    """
        Load all images by all users for moderation
    """

    # Find user record from database
    user = mongo.db.users.find_one({"username": session["user"]})
    admin = user["is_admin"]

    if session["admin"] == "true":

        # Find all posts and display in reverse added order
        images = mongo.db.images.find().sort("_id", -1)

        return render_template("manage_images.html", images=images)

    flash("You are not authorised to view this page and have been logged out")
    session.pop("user")
    return redirect(url_for("login"))
