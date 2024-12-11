from flask import Blueprint, render_template, abort, current_app

# Create the Blueprint
app_error = Blueprint("error", __name__, url_prefix="/error")


@app_error.app_errorhandler(401)
def unauthorised(e):
    return render_template("errors/unauthorised.html"), 401


@app_error.app_errorhandler(403)
def forbidden(e):
    return render_template("errors/forbidden.html"), 403


# Handle 404 errors
@app_error.app_errorhandler(404)
def page_not_found(e):  # Add 'e' to accept the error
    return (
        render_template("errors/page_not_found.html"),
        404,
    )  # Include status code 404 in the return


# Handle 500 errors
@app_error.app_errorhandler(500)
def internal_server_error(e):
    return render_template("errors/internal_server_error.html"), 500  # Add status code


# Trigger an error route
@app_error.route("/trigger_error")
def trigger_error():
    try:
        # Some operation that causes an error
        1 / 0  # This will cause a ZeroDivisionError
    except Exception as e:
        # Log the error using the application's logger
        current_app.logger.error(f"An error occurred: {e}")
        # Raise a 500 Internal Server Error
        abort(403)
