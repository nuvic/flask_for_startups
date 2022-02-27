# Standard Library imports

# Core Flask imports

# Third-party imports


def init_routes(app, db, login_manager):
    """
    app: instance of flask app
    db: DatabaseManager.session
    login_manager: flask_login extension class
    """

    # App imports (placed here to avoid circular import)
    from .views import (
        error_views,
        account_management_views,
        static_views,
    )
    from .models import User

    # Request management
    @app.before_request
    def before_request():
        db()

    @app.teardown_appcontext
    def shutdown_session(response_or_exc):
        db.remove()

    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID."""
        if user_id and user_id != "None":
            return User.query.filter_by(user_id=user_id).first()

    # Error views
    app.register_error_handler(404, error_views.not_found_error)

    app.register_error_handler(500, error_views.internal_error)

    # Public views
    app.add_url_rule("/", view_func=static_views.index)

    app.add_url_rule("/register", view_func=static_views.register)

    app.add_url_rule("/login", view_func=static_views.login)

    # Login required views
    app.add_url_rule("/settings", view_func=static_views.settings)

    # Public API
    app.add_url_rule(
        "/api/login", view_func=account_management_views.login_account, methods=["POST"]
    )

    app.add_url_rule("/logout", view_func=account_management_views.logout_account)

    app.add_url_rule(
        "/api/register",
        view_func=account_management_views.register_account,
        methods=["POST"],
    )

    # Login Required API
    app.add_url_rule("/api/user", view_func=account_management_views.user)

    app.add_url_rule(
        "/api/email", view_func=account_management_views.email, methods=["POST"]
    )

    # Admin required
    app.add_url_rule("/admin", view_func=static_views.admin)

    return
