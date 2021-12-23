"""
Imprint Nov 2021
Routes for all pages
"""

# Import dependencies, Flask and Werkzeug
from flask import (
    Blueprint,
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

# Import local code and config files
from forms import (
    RegisterForm,
    LoginForm,
    ChangePasswordForm,
    DeleteProfileForm,
    UploadImageForm,
    EditImageForm
    )
from config.cloudinary_config import *
# Using import * is generally frowned upon as a practice but this app is very
# simple, so it has been adopted in this case

# Get PyMongo instance
from config.database import mongo

# Initiate Blueprint
users = Blueprint(
    "users", __name__,
    static_folder="static",
    template_folder="templates"
)


# Define functions for use in user authentication
def is_logged_in():
    """
    Check if user is logged in, return username or none if not
    """
    return session.get("user")


def is_admin():
    """
    Check if user is logged in, return True or False, or none if not logged in
    """
    return session.get("admin")


# Route for Registration form
@users.route("/register", methods=["GET", "POST"])
def register():
    """
    Register form:
    Define which form to use
    Check request type and either load page,
    or validate, compare passwords and create document in DB
    """
    # Check if user already logged in
    if is_logged_in() is None:
        # Define form to use
        form = RegisterForm()
        # If request type is POST, check all fields are validated
        if form.validate_on_submit():
            # Check for existing username
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})
            # If username is taken, ask user to choose a different name
            if existing_user:
                flash("Username taken, please choose again")
                return redirect(url_for("users.register"))
            # Create dictionary with user form data and obscure password
            register_user = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(
                    request.form.get("password")),
                "is_admin": False
            }
            # Add user document to DB
            mongo.db.users.insert_one(register_user)

            # Create session cookie for user
            session["user"] = request.form.get("username").lower()
            session["admin"] = False

            # Feedback success to user and direct to About page
            flash(
                f"Welcome {register_user['username']}, thank you for joining!")
            return redirect(url_for("general.about"))

        # If request type is GET, render the about page accordingly
        return render_template("register.html", form=form)
    # If user already logged in flash message and return to Gallery page
    flash("You cannot register as you are already signed in")
    return redirect(url_for("general.gallery"))


# Route for login form
@users.route("/login", methods=["GET", "POST"])
def login():
    """
    Login form:
    Define which form to use
    Check request type and either load page,
    or validate, compare form data to DB and create session cookie
    """
    # Check if user already logged in
    if is_logged_in() is None:
        # Define form to use
        form = LoginForm()
        # If request type is POST, check all fields are validated
        if form.validate_on_submit():
            # Search for username in DB
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})
            if not existing_user:
                # If username entered does not exist, feedback to user
                flash("Invalid username, please try again")
                return render_template('login.html', form=form)
            else:
                # If username does exist, check entered password against DB
                if check_password_hash(
                        existing_user["password"],
                        request.form.get("password")):
                    # Put user and admin status into session
                    session["user"] = request.form.get("username")
                    session["admin"] = existing_user["is_admin"]
                    # Inform user of succesful login
                    flash(f"Welcome back {request.form.get('username')}")
                    # If admin, display such to user
                    if is_admin():
                        flash("You are signed in as an Administrator")

                # If password does not match DB, feedback to user
                else:
                    flash("Invalid password, please try again")
                    return render_template('login.html', form=form)

            # Redirect succesful login to gallery page
            return redirect(url_for("general.gallery"))

        # If request type is GET, render the about page accordingly
        return render_template('login.html', form=form)
    # If user already logged in flash message and return to Gallery page
    flash("You cannot login as you are already signed in")
    return redirect(url_for("general.gallery"))


# Route for logout
@users.route("/logout")
def logout():
    """
    Remove session cookie and feedback to user
    Redirect to login page
    """
    # Check if user logged in
    if is_logged_in():
        # Delete user session
        flash("You have successfully been logged out")
        session.pop("user")
        return redirect(url_for("users.login"))
    # If user not logged in flash message and return to login page
    flash("You cannot log out as you are not signed in")
    return redirect(url_for("users.login"))


# Route for profile page
@users.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Change password form:
    Define which form to use
    Check request type and either load page, or validate,
     compare old password to DB, check new passwords match and update DB
    Also displays all posts by user in gallery format
    """
    # Check if user logged in
    if is_logged_in():
        # Define form to use
        form = ChangePasswordForm()
        # Find user record from database
        user = mongo.db.users.find_one({"username": session["user"]})
        username = user["username"]
        # Find posts made by user
        images = mongo.db.images.find({"owner": username}).sort("_id", -1)

        # If request type is POST, check all fields are validated
        if form.validate_on_submit():
            # Check DB value matches that entered for old password in form
            if check_password_hash(
                    user["password"], request.form.get("old_password")):
                # Create variable containing hashed new password
                update_password = generate_password_hash(
                    request.form.get("new_password"))
                # Update DB document with new password
                mongo.db.users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"password": update_password}}
                )
                # Feedback success to user and return to profile page
                return render_template(
                    'profile.html',
                    username=username,
                    success=True
                )

            # If entered old password does not match DB ask to try again
            flash("Incorrect existing password, please try again")

        # If request type is GET, render the user profile page
        return render_template(
            "profile.html",
            images=images,
            username=username,
            form=form
        )
    # If user not logged in flash message and return to login page
    flash("Please login to manage your profile")
    return redirect(url_for("users.login"))


# Route to delete profile
@users.route("/delete_profile", methods=["GET", "POST"])
def delete_profile():
    """
    Get user information, delete all their posts and profile
    """
    # Check if user logged in
    if is_logged_in():
        # Define form to use
        form = DeleteProfileForm()
        # Find user record from database
        user = mongo.db.users.find_one({"username": session["user"]})
        username = user["username"]
        # Find posts made by user
        posts = mongo.db.images.find({"owner": username})

        # If request type is POST, check all fields are validated
        if form.validate_on_submit():
            # Check DB value matches that entered for password in form
            if check_password_hash(
                    user["password"], request.form.get("old_password")):
                # Delete user posts
                for post in posts:
                    # Remove images from Cloudinary and clear Cloudinary cache
                    cloudinary.uploader.destroy(
                        post["cloudinary_id"], invalidate=True)
                    # Remove documents from DB
                    mongo.db.images.remove({"_id": post["_id"]})
                # Remove session cookie
                session.pop("user")
                # Delete profile
                mongo.db.users.remove({"_id": user["_id"]})
                # Inform user and return to gallery page
                flash("Profile deleted successfully")
                return redirect(url_for("general.gallery"))

            # If entered password does not match DB ask to try again
            flash("Incorrect password, please try again")

        # If request type is GET, render the delete profile page
        return render_template("delete_profile.html", form=form)
    # If user not logged in flash message and return to login page
    flash("Please login to manage your profile")
    return redirect(url_for("users.login"))


# Route for upload page
@users.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Upload form:
    Define form to use
    Get locations for dropdown selector
    Take form data and create Cloudinary and DB entries
    """
    # Check if user logged in
    if is_logged_in():
        # Define form to use
        form = UploadImageForm()
        # Get location options and populate choices in upload form
        all_locations = mongo.db.locations.distinct('location_name')
        form.location.choices = list(all_locations)
        # Find user record from database
        user = mongo.db.users.find_one({"username": session["user"]})
        username = user["username"]

        # If request type is POST, check all fields are validated
        if form.validate_on_submit():
            # Send image to Cloudinary account and determine upload preset
            photo = request.files['photo']
            photo_upload = cloudinary.uploader.unsigned_upload(
                photo, "p6tbiahk")
            # Create dictionary for upload to DB as document
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
            # If successful, feedback to user and display choices
            return render_template('upload.html', success=True)

        # If request type is GET, render the upload page
        return render_template("upload.html", form=form)
    # If user not logged in flash message and return to login page
    flash("Please login or register for an account to add Gallery images")
    return redirect(url_for("users.login"))


# Route to edit a post
@users.route("/edit_image/<image_id>", methods=["GET", "POST"])
def edit_image(image_id):
    """
    Edit post form:
    Define form to use
    Use document id from profile page to get image data
    Make available for changes
    Update DB
    """
    # Get image document id
    image = mongo.db.images.find_one({"_id": ObjectId(image_id)})
    # Check if user logged in
    if is_logged_in():
        # Check if logged in user owns image or is admin
        if is_logged_in() == image["owner"] or is_admin():
            # Define form to use and populate with existing DB info
            form = EditImageForm(
                location=image["location"],
                decade=image["decade"],
                details=image["details"],
                tags=image["tags"]
            )
            # Get location options to populate dropdown in edit form
            all_locations = mongo.db.locations.distinct('location_name')
            form.location.choices = list(all_locations)

            # If request type is POST, check all fields are validated
            if form.validate_on_submit():
                # Get form and unchanged image values and make dictionary
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
                # Feedback to user and display changes
                flash("Post updated succesfully!")
                return render_template(
                    'edit_image.html', image=image, success=True)

            # If request type is GET, render the edit post page
            return render_template("edit_image.html", image=image, form=form)
        # If user not image owner flash message, logout and return login page
        flash(
            "You are not authorised to view this page and were signed out")
        session.pop("user")
        return redirect(url_for("users.login"))
    # If user not logged in return to login page
    flash("Please login to manage your profile")
    return redirect(url_for("users.login"))


# Route to delete a post
@users.route("/delete_image/<image_id>")
def delete_image(image_id):
    """
    Delete a post
    """
    # Get image from database
    image = mongo.db.images.find_one({"_id": ObjectId(image_id)})
    # Check if user logged in
    if is_logged_in():
        # Check if logged in user owns image or is admin
        if is_logged_in() == image["owner"] or is_admin():
            # Find user record from database
            user = mongo.db.users.find_one({"username": session["user"]})
            username = user["username"]
            # Remove document from DB
            mongo.db.images.remove({"_id": image["_id"]})
            # Remove image from Cloudinary and clear Cloudinary cache
            cloudinary.uploader.destroy(
                image["cloudinary_id"], invalidate=True)

            # Find posts made by user and define form for loading profile page
            images = mongo.db.images.find({"owner": username})
            form = ChangePasswordForm()

            # Inform user of success
            flash("Post succesfully deleted")

            # If admin return to manage images page
            if is_admin():
                return redirect(url_for("admin.manage_images"))
            # If regular user, return to profile page
            return render_template(
                "profile.html",
                images=images,
                username=username,
                form=form
            )

        # If user not image owner flash message, logout and return login page
        flash("You are not authorised to view this page and were signed out")
        session.pop("user")
        return redirect(url_for("users.login"))
    # If user not logged in return to login page
    flash("Please login to manage your profile")
    return redirect(url_for("users.login"))
