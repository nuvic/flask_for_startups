# Standard Library imports

# Core Flask imports

# Third-party imports

# App imports


def get_validation_error_response(validation_error, http_status_code, display_error=""):
    resp = {
        "errors": {
            "display_error": display_error,
            "field_errors": validation_error.errors()
        }
    }
    return resp, http_status_code


def get_business_requirement_error_response(business_logic_error, http_status_code):
    resp = {
        "errors": {
            "display_error": business_logic_error.message,
            "internal_error_code": business_logic_error.internal_error_code,
        }
    }
    return resp, http_status_code


def get_db_error_response(db_error, http_status_code):
    resp = {
        "errors": {
            "display_error": db_error.message,
            "internal_error_code": db_error.internal_error_code,
        }
    }
    return resp, http_status_code
