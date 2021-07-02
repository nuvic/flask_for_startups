# Standard Library imports

# Core Flask imports
from flask import render_template
from flask_login import login_required

# Third-party imports

# App imports


def index():
    return render_template('index.html')

def register():
    return render_template('register.html')

def login():
    return render_template('login.html')

@login_required
def settings():
    return render_template('settings.html')