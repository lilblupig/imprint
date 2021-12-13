"""
    Imprint Nov 2021
    Routes for error handlers
"""

from flask import (
    flash,
    render_template,
    url_for
)

# Import local Forms code
from app import app

@app.errorhandler(404)
def error_page_not_found(error):
    """ Error handler for 404 """
    message = "Sorry, we can't find that page"
    user_help = "Choose from the buttons below, or the main menu to get back on track."
    return render_template('errors.html', message=message, help=help), 404


@app.errorhandler(500)
def error_internal_server(error):
    """ Error handler for 500 """
    message = "Sorry, we seem to be experiencing some difficulty."
    user_help = "Choose from the buttons below, or the main menu to get back on track."
    return render_template('errors.html', message=message, help=help), 500


@app.errorhandler(Exception)
def error_generic(error):
    """ Error handler for all other exceptions """
    message = "Sorry, something went wrong."
    user_help = "Choose from the buttons below, or the main menu to get back on track."
    return render_template('errors.html', message=message, help=help), 500
