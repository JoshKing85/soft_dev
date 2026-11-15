from flask import  Blueprint, render_template, session, redirect, url_for
from src.services.dashboard_service import get_dashboard_data

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")

def dashboard():
    
    user_id = session.get("user_id")
    
    if user_id is None:
        redirect(url_for("login"))
        
    data = get_dashboard_data(user_id)

    return render_template("dashboard.html", dashboard_data=data)
    