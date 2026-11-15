from flask import Blueprint, render_template

development_bp = Blueprint("dev_page", __name__)

@development_bp.route("/development")
def dev_page():
    return render_template("under_development.html")