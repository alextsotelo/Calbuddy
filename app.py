"""CalBuddy's web entry point. The terminal entry point remains main.py."""

from flask import Flask, render_template
from meal_routes import meals_bp


def create_app():
    """Construct the web application and register its first route."""
    app = Flask(__name__)
    app.register_blueprint(meals_bp)

    @app.get("/")
    def home():
        """Render the home template using a greeting supplied by Python."""
        return render_template("home.html", greeting="Welcome to CalBuddy!")

    return app


if __name__ == "__main__":
    # Start the local development server when running this file directly.
    create_app().run(debug=True)
