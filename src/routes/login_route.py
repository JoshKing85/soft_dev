from flask import (
    Blueprint, 
    render_template, 
    request, 
    url_for, 
    session, 
    redirect, 
    current_app,
    make_response)

from src.services.authentication_service import (
    auth_login,
    gen_token)

login_bp = Blueprint("login", __name__)

@login_bp.route("/login-page", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Valdiate email and password input and verify user ID existance.
        user_id = auth_login(email, password)

        if user_id is not None:
            session.clear()
            session["user_id"] = user_id
            
            # Generate JWT for cookie
            token = gen_token(
                user_id,
                 current_app.config["JWT_SECRET_KEY"] )
            
            response = make_response(redirect(url_for("dashboard.dashboard")))

            # Attach JWT to the response as a secure, HttpOnly browser cookie
            response.set_cookie(
                "access_token",
                token,
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=3600
            )
            return response

        return render_template(
            "login.html",
            error="Incorrect email or password"
        )