
from flask import (
    Blueprint,
    request,
    render_template,
    url_for,
    session,
    redirect,
    abort,
    flash
)
from src.middleware.create_goal_validator import validate_create_goal
from src.middleware.jwt_auth import validate_jwt
from datetime import date, timedelta

from src.services.goal_service import (
    get_current_model,
    get_points_model,
    create_goal,
    update_goal
)



goals_bp = Blueprint("goals", __name__)


@goals_bp.route("/goals", methods=["GET", "POST"])
@validate_jwt
def goals():

    # Authentication guard
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login.login"))

    # Handle goal creation and updates
    if request.method == "POST":

        action = request.form.get("action")

        if action == "create":
            success, message = create_goal(user_id, request.form.to_dict())
            if success:
                flash(message, "success")
            else:
                flash(message, "error")

        elif action == "update":
            update_goal(user_id, request.form.to_dict())

        else:
            abort(400)

        return redirect(url_for("goals.goals"))

    # Calculate 30-day goal period
    start_date = date.today()
    end_date = start_date + timedelta(days=30)

    # Retrieve presentation models
    current_model = get_current_model(user_id)
    points_model = get_points_model(user_id)

    # Render Goals page
    return render_template(
        "goals.html",
        current=current_model,
        points=points_model,
        start_date=start_date,
        end_date=end_date
    )
