# Standard Library imports

# Core Flask imports
from flask import render_template

# Third-party imports

# App imports


def not_found_error(error):
    return render_template("404.html"), 404


def internal_error(error):
    return render_template("500.html"), 500
