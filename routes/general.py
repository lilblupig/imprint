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
general = Blueprint(
    "general", __name__,
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


# Default route for homepage
@general.route("/")
@general.route("/gallery")
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
@general.route("/image_search", methods=["GET", "POST"])
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
@general.route("/location_filter", methods=["GET", "POST"])
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
@general.route("/single_image/<image_id>")
def single_image(image_id):
    """
    Use document id passed from gallery page to display single image and info
    """
    # Get image using document id
    image = mongo.db.images.find_one({"_id": ObjectId(image_id)})

    # Render the image in large view with details below
    return render_template("single_image.html", image=image)


# Route for About page
@general.route("/about")
def about():
    """
    Get about page and render different buttons if logged in/out
    """
    return render_template("about.html")


# Route for Contact Form
@general.route("/contact", methods=["GET", "POST"])
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
        return redirect(url_for("general.gallery"))
    # If request type is GET, render the contact form
    return render_template("contact.html", form=form)
