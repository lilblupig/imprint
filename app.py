"""
Imprint Nov 2021
Master module
"""

# Import dependencies
import os
from flask import Flask
from flask_talisman import Talisman

# Import Blueprints
from routes.admin import admin
from routes.general import general
from routes.users import users
from routes.errors import errors

# Get PyMongo instance
from config.database import mongo

# Get environment variables
if os.path.exists("config/env.py"):
    from config import env

# Initiate Flask application
app = Flask(__name__)

# Define database access variables
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Define ReCaptcha secret keys
app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ.get("C_SITE_KEY")
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get("C_SECRET_KEY")

# Blueprints
# Blueprints for general app
app.register_blueprint(admin)
app.register_blueprint(general)
app.register_blueprint(users)
# Blueprint for errors
app.register_blueprint(errors)

# Initialise database
mongo.init_app(app)

# Wrap Flask app with Talisman
Talisman(app, content_security_policy=None)

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=False
    )
