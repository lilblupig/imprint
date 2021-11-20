"""
    Imprint Nov 2021
    Master module
"""

# Import dependencies
import os
from flask import Flask
from flask_pymongo import PyMongo

# Get environment variables
if os.path.exists("config/env.py"):
    from config import env

# Initiaite Flask application
app = Flask(__name__)

# Define database access variables
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Define ReCaptcha secret keys
app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ.get("C_SITE_KEY")
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get("C_SECRET_KEY")

# Get routes
from routes.routes import *

# Set PyMongo variable
mongo = PyMongo(app)

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
