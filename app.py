""" Import dependencies """
import os
from flask import (
    Flask,
    flash,
    render_template,
    redirect,
    request,
    session,
    url_for
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message, Mail
if os.path.exists("env.py"):
    import env
from forms import ContactForm

mail = Mail()

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ.get("C_SITE_KEY")
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get("C_SECRET_KEY")

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

mail.init_app(app)

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_locations")
def get_locations():
    """ Define test function """
    locations = mongo.db.locations.find()
    return render_template("index.html", locations=locations)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """ Contact form """
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            return 'Form posted.'
    elif request.method == 'GET':
        return render_template(
            "contact.html",
            form=form,
        )


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
