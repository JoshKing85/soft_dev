
from flask import Flask
from src.routes.landing_route import landing_bp
from src.routes.dev_page_route import development_bp
from src.routes.login_route import login_bp
from src.routes.signup_route import signup_bp
from src.routes.dashboard_route import dashboard_bp
from src.routes.goals_route import goals_bp

app = Flask(
    __name__,
    template_folder="src/templates",
    static_folder="src/static"
)
app.secret_key = "temporary-development-key"
app.config["JWT_SECRET_KEY"] = app.secret_key

app.register_blueprint(landing_bp)
app.register_blueprint(development_bp)
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(goals_bp)

if __name__ == "__main__":
    app.run(debug=True)
