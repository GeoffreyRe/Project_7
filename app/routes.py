"""
This module contains view functions of this flask app
"""
from flask import render_template, request
from app import app # we import app variable
import app.grandpybot as grandpybot

"""
we use the decorator "@app.route" to link the url given
as a parameter to the views function below
"""
@app.route("/")
@app.route("/GrandPyBot")
def grandpy_bot_template():
    """
    This view function return a rendered template which is grandpy.html
    """
    return render_template("grandpy.html")

@app.route("/answer", methods=["GET", "POST"])
def grandpy_answer():
    """
    this view function return the response from grandpy
    """
    if request.method == "POST":
        input_value = request.data.decode("utf-8")
        grandpy_bot = grandpybot.GrandpyBot()

        return grandpy_bot.answer_to_user(input_value)
