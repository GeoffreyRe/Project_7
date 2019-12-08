from app import app # we import app variable
from flask import render_template, request
import time, app.utils.ApiUser as ApiUser

"""
we use the decorator "@app.route" to link the url given
as a parameter to the views function below
"""
@app.route("/")
@app.route("/GrandPyBot")
def grandpy_bot():
	return render_template("grandpy.html")

@app.route("/test", methods=["GET", "POST"])
def fonction_test():
	api = ApiUser.ApiUser()
	api.set_place_to_find("la chapelle sixtinne")
	api.find_all_informations()
	if request.method == "POST":
		print(request.data.decode("utf-8"))
		time.sleep(2)
		return api.give_informations()[1]

