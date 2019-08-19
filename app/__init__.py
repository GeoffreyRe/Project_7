from flask import Flask #We import the Flask class from flask

"""
This is the instance of our application. It is an instance of Flask and we have to
give the __name__ variable as a parameter because flask uses the location of this module to
find some ressources such as templates,...
"""
app = Flask(__name__)

from app import routes