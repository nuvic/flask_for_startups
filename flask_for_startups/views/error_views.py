# Standard Library imports

# Core Flask imports
from flask import render_template

# Third-party imports

# App imports
from flask_for_startups.utils.error_utils import get_permission_error_response, get_db_error_response
from flask_for_startups.utils.custom_errors import InternalDbError

def internal_db_error(error):
    return get_db_error_response(db_error=InternalDbError, http_status_code=500)

def permission_denied_error(error):
    return get_permission_error_response(permission_error=error, http_status_code=403)

def not_found_error(error):
    return render_template('404.html'), 404

def internal_error(error):
    return render_template('500.html'), 500