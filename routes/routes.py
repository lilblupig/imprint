"""
Imprint Nov 2021
Routes for all pages
"""

# Import dependencies, Flask and Werkzeug
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

# Import local code and config files
from app import app, mongo
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


# Default route for homepage
@app.route("/")
@app.route("/gallery")
def gallery():
    """
    Get locations and images from DB
    Display gallery/home page
    """
    # Get all locations for filter box
    locations = mongo.db.locations.find()
    # Get images from database
    images = mongo.db.images.find().sort("_id", -1)
    # Get maps key from environment variables
    maps_key = os.environ.get("MAPS_KEY")

    # Render all images in gallery format
    return render_template("gallery.html", images=images, locations=locations, maps_key=maps_key)


# Route for gallery free text search
@app.route("/image_search", methods=["GET", "POST"])
def image_search():
    """
    Collect info from search input and use DB index to return results
    Display on gallery/home page
    """
    # Get all locations for filter box
    locations = mongo.db.locations.find()
    # Get search form data
    image_request = request.form.get("image_search")
    # Get maps key from environment variables
    maps_key = os.environ.get("MAPS_KEY")
    # Search database using permanent text index
    images = mongo.db.images.find({"$text": {"$search": image_request}})

    # If DB search yields no results, flash user message
    if mongo.db.images.count_documents({"$text": {"$search": image_request}}) < 1:
        flash("No results found")

    # Render the search results in gallery form
    return render_template("gallery.html", images=images, locations=locations, maps_key=maps_key)


# Route for gallery dropdown filter
@app.route("/location_filter", methods=["GET", "POST"])
def location_filter():
    """
    Collect info from dropdown and query DB for results
    Display on gallery/home page
    """
    # Get all locations for filter box
    locations = mongo.db.locations.find()
    # Get dropdown field data
    location_choice = request.form.get("location_filter")
    # Get maps key from environment variables
    maps_key = os.environ.get("MAPS_KEY")
    # Query DB for appropriate documents
    images = mongo.db.images.find({"location": location_choice})

    # If DB search yields no results, flash user message
    if mongo.db.images.count_documents({"location": location_choice}) < 1:
        flash(location_choice)

    # Render the filtered results in gallery form
    return render_template("gallery.html", images=images, locations=locations, location_choice=location_choice, maps_key=maps_key)


# Route for displaying Single Image
@app.route("/single_image/<image_id>")
def single_image(image_id):
    """
    Use document id passed from gallery page to display single image and info
    """
    # Get image using document id
    image = mongo.db.images.find_one({"_id": ObjectId(image_id)})

    # Render the image in large view with details below
    return render_template("single_image.html", image=image)


# Route for About page
@app.route("/about")
def about():
    """
    Get about page and render different buttons if logged in/out
    """
    return render_template("about.html")


# Route for Contact Form
@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Contact form:
    Define which form to use
    Check request type and either load page,
    or validate, create message and send form
    """
    # Define form to use
    form = ContactForm()
    # If request type is POST, check all fields are validated
    if form.validate_on_submit():
        # Get form data and put in dictionary
        form_content = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "body": request.form.get("body")
        }

        # Call mail function and provide form data
        try:
            mail_config.send_email(form_content)
        # If unable to send, flash failure message
        except Exception as e:
            flash("Unable to send email, please try again later")
        # Otherwise, flash success message
        else:
            flash("Thank you for your message, we will be in touch as soon as we can.")

        # Redirect user to gallery page
        return redirect(url_for("gallery"))

    # If request type is GET, render the contact form
    return render_template("contact.html", form=form)


# Route for Registration form
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register form:
    Define which form to use
    Check request type and either load page,
    or validate, compare passwords and create document in DB
    """
    # Define form to use
    form = RegisterForm()
    # If request type is POST, check all fields are validated
    if form.validate_on_submit():
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
            "is_admin": False
        }
        # Add user document to DB
        mongo.db.users.insert_one(register_user)

        # Create session cookie for user
        session["user"] = request.form.get("username").lower()
        session["admin"] = False

        # Feedback success to user and direct to About page
        flash(f"Welcome {register_user['username']}, thank you for joining!")
        return redirect(url_for("about"))

    # If request type is GET, render the about page accordingly
    return render_template("register.html", form=form)


# Route for login form
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login form:
    Define which form to use
    Check request type and either load page,
    or validate, compare form data to DB and create session cookie
    """
    # Define form to use
    form = LoginForm()
    # If request type is POST, check all fields are validated
    if form.validate_on_submit():
        # Search for username in DB
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})
        if not existing_user:
            # If username entered does not exist, feedback to user
            flash("Invalid username, please try again")
            return render_template('login.html', form=form)
        else:
            # If username does exist, check entered password against DB
            if check_password_hash(existing_user["password"], request.form.get("password")):
                # Put user and admin status into session
                session["user"] = request.form.get("username")
                session["admin"] = existing_user["is_admin"]
                # Inform user of succesful login
                flash(f"Welcome back {request.form.get('username')}")
                # If admin, display such to user
                if session["admin"] == True:
                    flash("You are signed in as an Administrator")

            # If password does not match DB, feedback to user
            else:
                flash("Invalid password, please try again")
                return render_template('login.html', form=form)

        # Redirect succesful login to gallery page
        return redirect(url_for("gallery"))

    # If request type is GET, render the about page accordingly
    return render_template('login.html', form=form)


# Route for logout
@app.route("/logout")
def logout():
    """
    Remove session cookie and feedback to user
    Redirect to login page
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
    Check request type and either load page,
    or validate, compare old password to DB, check new passwords match and update DB
    Also displays all posts by user in gallery format
    """
    # Define form to use
    form = ChangePasswordForm()
    # Find user record from database
    user = mongo.db.users.find_one({"username": session["user"]})
    username = user["username"]
    # Find posts made by user
    images = mongo.db.images.find({"owner": username})

    # If request type is POST, check all fields are validated
    if form.validate_on_submit():
        # Check DB value matches that entered for old password in form
        if check_password_hash(user["password"], request.form.get("old_password")):
            # Create variable containing hashed new password
            update_password = generate_password_hash(request.form.get("new_password"))
            # Update DB document with new password
            mongo.db.users.update_one({"_id": user["_id"]}, {"$set": {"password": update_password}})
            # Feedback success to user and return to profile page
            return render_template('profile.html', username=username, success=True)

        # If entered old password does not match DB ask to try again
        flash("Incorrect existing password, please try again")

    # If request type is GET, render the user profile page
    return render_template("profile.html", images=images, username=username, form=form)


# Route to delete profile
@app.route("/delete_profile", methods=["GET", "POST"])
def delete_profile():
    """
    Get user information, delete all their posts and profile
    """
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
        if check_password_hash(user["password"], request.form.get("old_password")):
            # Delete user posts
            for post in posts:
                # Remove images from Cloudinary and clear Cloudinary cache
                cloudinary.uploader.destroy(post["cloudinary_id"], invalidate=True)
                # Remove documents from DB
                mongo.db.images.remove({"_id": post["_id"]})
            # Remove session cookie
            session.pop("user")
            # Delete profile
            mongo.db.users.remove({"_id": user["_id"]})
            # Inform user and return to gallery page
            flash("Profile deleted successfully")
            return redirect(url_for("gallery"))

        # If entered password does not match DB ask to try again
        flash("Incorrect password, please try again")

    # If request type is GET, render the delete profile page
    return render_template("delete_profile.html", form=form)


# Route for upload page
@app.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Upload form:
    Define form to use
    Get locations for dropdown selector
    Take form data and create Cloudinary and DB entries
    """
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
        # Send image to Cloudinary account and determine upload preset to use
        photo = request.files['photo']
        photo_upload = cloudinary.uploader.unsigned_upload(photo, "p6tbiahk")
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


# Route to edit a post
@app.route("/edit_image/<image_id>", methods=["GET", "POST"])
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
    # Define form to use and populate with existing DB info
    form = EditImageForm(location=image["location"], decade=image["decade"], details=image["details"], tags=image["tags"])
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
        return render_template('edit_image.html', image=image, success=True)

    # If request type is GET, render the edit post page
    return render_template("edit_image.html", image=image, form=form)


# Route to delete a post
@app.route("/delete_image/<image_id>")
def delete_image(image_id):
    """
    Delete a post
    """
    # Find user record from database
    user = mongo.db.users.find_one({"username": session["user"]})
    username = user["username"]
    # Get image from database
    image = mongo.db.images.find_one({"_id": ObjectId(image_id)})

    # Check if a user is in session to try and avoid brute force access
    if session["user"] == image["owner"] or session["admin"] == True:
        # Remove document from DB
        mongo.db.images.remove({"_id": image["_id"]})
        # Remove image from Cloudinary and clear Cloudinary cache
        cloudinary.uploader.destroy(image["cloudinary_id"], invalidate=True)

        # Find posts made by user and define form for loading profile page
        images = mongo.db.images.find({"owner": username})
        form = ChangePasswordForm()

        # Inform user of success
        flash("Post succesfully deleted")

        # If admin return to manage images page
        if session["admin"] == True:
            return redirect(url_for("manage_images"))

        # If regular user, return to profile page
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
    # Check if user is admin
    if session["admin"] == True:
        # Find all users and display in alphabetical order
        users = mongo.db.users.find().sort("username", 1)
        return render_template("manage_users.html", users=users)

    # If not admin, log out and return to login page
    flash("You are not authorised to view this page and have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Route for Admin toggle
@app.route("/admin_toggle/<user_toggle_id>")
def admin_toggle(user_toggle_id):
    """
    Toggle on or off user admin permissions
    """
    # Check current logged in user has admin rights
    if session["admin"] == True:
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
        return redirect(url_for("manage_users"))

    # If not admin, log out and return to login page
    flash("You are not authorised to view this page and have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Route for admin to delete user profile
@app.route("/admin_delete_profile/<delete_user>", methods=["GET", "POST"])
def admin_delete_profile(delete_user):
    """
    Get user information, delete posts, and profile
    """
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
    if session["admin"] == True:
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
                return redirect(url_for("manage_users"))

        # If admin password incorrect, ask admin to try again
        flash("Incorrect password, please try again")

    # If request type is GET, render the delete profile page
    return render_template("admin_delete_profile.html", form=form, deleting_user=deleting_user)


# Route for Admin Image Management page
@app.route("/manage_images")
def manage_images():
    """
    Load all images by all users for moderation
    """
    # if user is admin, load all posts in gallery format
    if session["admin"] == True:
        # Find all posts and display in reverse added order
        images = mongo.db.images.find().sort("_id", -1)
        return render_template("manage_images.html", images=images)

    # If not admin, log out and return to login page
    flash("You are not authorised to view this page and have been logged out")
    session.pop("user")
    return redirect(url_for("login"))
