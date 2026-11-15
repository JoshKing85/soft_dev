
from flask import Blueprint, render_template, request, session, redirect, url_for
from src.middleware.reg_limiter import reg_limiter
from src.middleware.reg_form_validator import validate_registration_form

from src.services.registration_service import (
    validate_registration,
    registration
)

signup_bp = Blueprint("signup", __name__)


@signup_bp.route("/sign-up", methods=["GET", "POST"])
@reg_limiter.limit("10 per minute", methods=["POST"])
@validate_registration_form
def signup():

    registration_data = session.get("registration_data", {})

    # GET: Display requested stage
    if request.method == "GET":

        step = request.args.get("step", 1, type=int)

        if step not in (1, 2, 3, 4):
            step = 1

        # Prevent skipping incomplete stages
        if step > 1 and not registration_data.get("user_data"):
            step = 1

        elif step > 2 and not registration_data.get("membership"):
            step = 2

        elif step > 3 and not registration_data.get("fitness"):
            step = 3

        # Retrieve appropriate data
        if step == 1:
            form_data = registration_data.get("user_data", {})

        elif step == 2:
            form_data = registration_data.get("membership", {})

        elif step == 3:
            form_data = registration_data.get("fitness", {})

        else:
            form_data = registration_data

        return render_template(
            "signup.html",
            step=step,
            registration_data=form_data
        )

    # POST: Process submitted form
    step = request.form.get("step", 1, type=int)

    # Stage 1: User Details
    if step == 1:

        user_data = request.form.to_dict()
        user_data.pop("step", None)

        valid, error = validate_registration(user_data)

        if not valid:
            return render_template(
                "signup.html",
                step=1,
                error=error,
                registration_data=user_data
            )

        registration_data["user_data"] = user_data
        session["registration_data"] = registration_data

        return redirect(url_for("signup.signup", step=2))

    # Stage 2: Membership Selection
    elif step == 2:

        if not registration_data.get("user_data"):
            return redirect(url_for("signup.signup", step=1))

        membership_data = {
            "plan": request.form.get("membership_plan")
        }

        if membership_data["plan"] not in ("standard", "plus", "premium"):
            return render_template(
                "signup.html",
                step=2,
                error="Please select a membership plan.",
                registration_data=membership_data
            )

        registration_data["membership"] = membership_data
        session["registration_data"] = registration_data

        return redirect(url_for("signup.signup", step=3))

    # Stage 3: Fitness Survey
    elif step == 3:

        if not registration_data.get("user_data"):
            return redirect(url_for("signup.signup", step=1))

        if not registration_data.get("membership"):
            return redirect(url_for("signup.signup", step=2))

        fitness_data = request.form.to_dict()
        fitness_data.pop("step", None)

        fitness_data["exercise_types"] = request.form.getlist("exercise_types")
        fitness_data["classes"] = request.form.getlist("classes")

        registration_data["fitness"] = fitness_data
        session["registration_data"] = registration_data

        return redirect(url_for("signup.signup", step=4))

    # Stage 4: Confirmation
    elif step == 4:

        if not registration_data.get("user_data"):
            return redirect(url_for("signup.signup", step=1))

        if not registration_data.get("membership"):
            return redirect(url_for("signup.signup", step=2))

        if not registration_data.get("fitness"):
            return redirect(url_for("signup.signup", step=3))

        registration_data["advertising_consent"] = (
            request.form.get("advertising_consent") == "yes"
        )

        # Submit complete registration to service
        result = registration(registration_data)
        

        if not result["success"]:

            failed_step = result["step"]

            if failed_step == 1:
                form_data = registration_data["user_data"]

            elif failed_step == 2:
                form_data = registration_data["membership"]

            else:
                form_data = registration_data["fitness"]

            return render_template(
                "signup.html",
                step=failed_step,
                error=result["error"],
                registration_data=form_data
            )
        
        # Clear registration data after successful completion
        session.pop("registration_data", None)

        return redirect(url_for("signup.registration_success"))

    return redirect(url_for("signup.signup", step=1))



@signup_bp.route("/registration-success")
def registration_success():

    return render_template("registration_success.html")
