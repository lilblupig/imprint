"""
Imprint Nov 2021
Routes for error handlers
"""

from flask import (
    Blueprint,
    render_template
)

# Initiate Blueprint
errors = Blueprint(
    "errors", __name__,
    static_folder="static",
    template_folder="templates"
)

# Import local Forms code
from app import app


@errors.app_errorhandler(404)
def error_page_not_found(error):
    """ Error handler for 404 """
    message = "Sorry, we can't find that page"
    user_help = "Choose from the buttons below, or the main menu to get back on track."
    return render_template('errors.html', message=message, user_help=user_help), 404


@errors.app_errorhandler(500)
def error_internal_server(error):
    """ Error handler for 500 """
    message = "Sorry, we seem to be experiencing some difficulty."
    user_help = "Choose from the buttons below, or the main menu to get back on track."
    return render_template('errors.html', message=message, user_help=user_help), 500


@errors.app_errorhandler(Exception)
def error_generic(error):
    """ Error handler for all other exceptions """
    message = "Sorry, something went wrong."
    user_help = "Choose from the buttons below, or the main menu to get back on track."
    return render_template('errors.html', message=message, user_help=user_help), 500
