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

# Get PyMongo instance
from config.database import mongo

# Initiate Blueprint
admin = Blueprint(
    "admin", __name__,
    static_folder="static",
    template_folder="templates"
)

# Import Object ID info from MongoDB
from bson.objectid import ObjectId

# Import local code and config files
from forms import (
    ContactForm,
    RegisterForm,
    LoginForm,
    ChangePasswordForm,
    DeleteProfileForm,
    UploadImageForm,
    EditImageForm
    )
from config import mail_config
from config.cloudinary_config import *
# Using import * is generally frowned upon as a practice but this app is very simple, so it has been adopted in this case


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


# Route for Admin User Management page
@admin.route("/manage_users")
def manage_users():
    """
    Load all users for moderation
    """
    # Check if user logged in
    if is_logged_in():
        # Check if user is admin
        if is_admin():
            # Find all users and display in alphabetical order
            users = mongo.db.users.find().sort("username", 1)
            return render_template("manage_users.html", users=users)

        # If not admin, log out and return to login page
        flash("You are not authorised to view this page and have been logged out")
        session.pop("user")
        return redirect(url_for("users.login"))
    # If user not logged in return to login page
    flash("You are not authorised to view this page")
    return redirect(url_for("users.login"))


# Route for Admin toggle
@admin.route("/admin_toggle/<user_toggle_id>")
def admin_toggle(user_toggle_id):
    """
    Toggle on or off user admin permissions
    """
    # Check if user logged in
    if is_logged_in():
        # Check if user is admin
        if is_admin():
            # Find user to be toggled
            user_toggle = mongo.db.users.find_one({"_id": ObjectId(user_toggle_id)})
            # Check current admin status
            if user_toggle["is_admin"] == False:
                # Toggle admin rights on
                mongo.db.users.update_one({"_id": user_toggle["_id"]}, {"$set": {"is_admin": True}})
            else:
                # Toggle admin rights off
                mongo.db.users.update_one({"_id": user_toggle["_id"]}, {"$set": {"is_admin": False}})
            # Update admin on user management page
            flash("User updated succesfully!")
            return redirect(url_for("admin.manage_users"))

        # If not admin, log out and return to login page
        flash("You are not authorised to view this page and have been logged out")
        session.pop("user")
        return redirect(url_for("users.login"))
    # If user not logged in return to login page
    flash("You are not authorised to view this page")
    return redirect(url_for("users.login"))


# Route for admin to delete user profile
@admin.route("/admin_delete_profile/<delete_user>", methods=["GET", "POST"])
def admin_delete_profile(delete_user):
    """
    Get user information, delete posts, and profile
    """
    # Check if user logged in
    if is_logged_in():
        # Check if user is admin
        if is_admin():
            # Define form to use
            form = DeleteProfileForm()
            # Find admin user record from database
            user = mongo.db.users.find_one({"username": session["user"]})
            # Find user record from database
            deleting_user = mongo.db.users.find_one({"_id": ObjectId(delete_user)})
            deleting_username = deleting_user["username"]
            # Find posts made by user
            posts = mongo.db.images.find({"owner": deleting_username})

            # If request type is POST, check all fields are validated
            if form.validate_on_submit():
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
                    # Feedback to admin and return to manage posts page
                    flash("User deleted succesfully!")
                    return redirect(url_for("admin.manage_users"))

                # If admin password incorrect, ask admin to try again
                flash("Incorrect password, please try again")

            # If request type is GET, render the delete profile page
            return render_template("admin_delete_profile.html", form=form, deleting_user=deleting_user)
        # If not admin, log out and return to login page
        flash("You are not authorised to view this page and have been logged out")
        session.pop("user")
        return redirect(url_for("users.login"))
    # If user not logged in return to login page
    flash("You are not authorised to view this page")
    return redirect(url_for("users.login"))


# Route for Admin Image Management page
@admin.route("/manage_images")
def manage_images():
    """
    Load all images by all users for moderation
    """
    # Check if user logged in
    if is_logged_in():
        # Check if user is admin
        if is_admin():
            # Find all posts and display in reverse added order
            images = mongo.db.images.find().sort("_id", -1)
            return render_template("manage_images.html", images=images)

        # If not admin, log out and return to login page
        flash("You are not authorised to view this page and have been logged out")
        session.pop("user")
        return redirect(url_for("users.login"))
    # If user not logged in return to login page
    flash("You are not authorised to view this page")
    return redirect(url_for("users.login"))
