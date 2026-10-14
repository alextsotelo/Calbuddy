"""Web routes for meal features; database operations remain in crud.py."""

from flask import Blueprint, current_app, render_template

import crud


# "meals" names the group; it also prefixes its route endpoint names.
meals_bp = Blueprint("meals", __name__)


@meals_bp.get("/meals")
def list_meals():
    """Retrieve active meals and render them as an HTML table."""
    try:
        meals = crud.get_active_meals(raise_on_error=True)
    except RuntimeError:
        # Log details in the server console; show a readable message on the page.
        current_app.logger.exception("Unable to load meals")
        return render_template(
            "meals.html",
            meals=[],
            error="We couldn't load your meals. Check the database connection and try again.",
        ), 503

    return render_template("meals.html", meals=meals, error=None)
