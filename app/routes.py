from app import app # we import app variable

"""
we use this decorator to link the url given
as a parameter to the views function below
"""
@app.route("/")
def index():
	return "test"

