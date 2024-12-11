from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    get_flashed_messages,
)
from flask_login import login_required, login_user, logout_user, user_logged_in
from keys import FLASK_SESSION_KEY
from src.dbModels import User, dbSession
from src.security.oneway import generate_secure_hash

app_session = Blueprint("session", __name__, url_prefix="/session")


# Helper function for validations
def validate_sign_up_data(firstName, lastName, phone, email, password, confirm_pass):
    errors = []

    if not all([firstName, lastName, phone, email, password, confirm_pass]):
        errors.append("All fields are required.")
    if password != confirm_pass:
        errors.append("Passwords do not match.")
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if len(phone) != 10 or not phone.isdigit():
        errors.append("Enter a valid phone number of 10 digits.")
    if "@" not in email or "." not in email.split("@")[-1]:
        errors.append("Enter a valid email address.")

    return errors


@app_session.route("/")
def index():
    if user_logged_in:
        return redirect(url_for("page.home"))
    return redirect(url_for("session.login"))


@app_session.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = hash(request.form.get("password"))
        print(email, password)

        with dbSession() as dbsession:
            user = dbsession.query(User).filter(User.email == email).first()
            print(f"Queried User: {user}")
            if user and user.password != password:
                print(f"Password Mismatch: {user.password} != {password}")

        if user:
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for("page.home"))
        else:
            flash("Invalid email or password.", "warning")
            return redirect(url_for("session.login"))

    return render_template("session/login.html")


@app_session.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirm")

        errors = validate_sign_up_data(
            firstName, lastName, phone, email, password, confirm_pass
        )
        if errors:
            for error in errors:
                flash(error, "info")
            return redirect(url_for("session.sign_up"))

        password_hashed = generate_secure_hash(password)
        with dbSession() as dbsession:
            existing_user = (
                dbsession.query(User)
                .filter((User.email == email) | (User.phone == phone))
                .first()
            )

            if existing_user:
                if existing_user.email == email:
                    flash("Email already exists.", "info")
                if existing_user.phone == phone:
                    flash("Phone number already exists.", "info")
                return redirect(url_for("session.sign_up"))

            # Add new user
            new_user = User(
                firstName=firstName,
                lastName=lastName,
                email=email,
                phone=phone,
                password=password_hashed,
            )
            try:
                dbsession.add(new_user)
                dbsession.commit()
                flash("Successfully registered.", "success")
                return redirect(url_for("session.login"))
            except Exception as e:
                dbsession.rollback()
                flash("Error: Registration failed.", "danger")
                print(f"Error during registration: {e}")
                return redirect(url_for("session.sign_up"))

    return render_template("session/sign_up.html")


@app_session.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("session.login"))
