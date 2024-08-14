from flask import Flask, render_template, request, session, url_for, redirect
from flask_session import Session
from utils.calculations import calculate_points
from config import SECRET_KEY, SESSION_TYPE, DEBUG

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SESSION_TYPE"] = SESSION_TYPE
Session(app)


@app.route("/", methods=["GET", "POST"])
def calculator():
    if "lineup" not in session:
        session["lineup"] = {
            "QB": {"name": "", "points": 0},
            "RB1": {"name": "", "points": 0},
            "RB2": {"name": "", "points": 0},
            "WR1": {"name": "", "points": 0},
            "WR2": {"name": "", "points": 0},
            "DEF": {"name": "", "points": 0},
            "K": {"name": "", "points": 0},
            "FLEX": {"name": "", "points": 0},
        }

    if request.method == "POST":
        if "calculate" in request.form:
            player_name = request.form["player_name"]
            player_type = request.form["player_type"]  # noqa: F841
            points = calculate_points(request.form)

            return render_template(
                "calculator.html",
                player_name=player_name,
                points=points,
                lineup=session["lineup"],
            )

        elif "save_to_lineup" in request.form:
            player_name = request.form["player_name"]
            points = float(request.form["points"])
            position = request.form["position"]

            session["lineup"][position] = {"name": player_name, "points": points}
            session.modified = True

    total_score = sum(player["points"] for player in session["lineup"].values())
    return render_template(
        "calculator.html", lineup=session["lineup"], total_score=total_score
    )


@app.route("/reset_lineup", methods=["POST"])
def reset_lineup():
    session["lineup"] = {
        "QB": {"name": "", "points": 0},
        "RB1": {"name": "", "points": 0},
        "RB2": {"name": "", "points": 0},
        "WR1": {"name": "", "points": 0},
        "WR2": {"name": "", "points": 0},
        "DEF": {"name": "", "points": 0},
        "K": {"name": "", "points": 0},
        "FLEX": {"name": "", "points": 0},
    }
    session.modified = True
    return redirect(url_for("calculator"))


if __name__ == "__main__":
    app.run(debug=DEBUG)
