# Standard Library imports

# Core Flask imports
from flask_login import current_user

# Third-party imports

# App imports
from flask_for_startups.utils import custom_errors


def permissions_list(permission_constants_list):
    # permission_constants_list is a list of constants where each constant is a function
    # each permission function:
    #   * raise PermissionsDeniedError if user does not have permission
    try:
        for permission_fx in permission_constants_list:
            permission_fx(current_user)
    except custom_errors.PermissionsDeniedError:
        raise custom_errors.PermissionsDeniedError
    return

def admin_required(current_user_model):
    role_to_check = 'admin'
    if role_to_check not in current_user_model.roles:
        raise custom_errors.PermissionsDeniedError
    return


ADMIN = admin_required