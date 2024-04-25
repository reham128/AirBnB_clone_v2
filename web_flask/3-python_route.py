#!/usr/bin/python3
"""Starts a Flask web application.
The application listens on 0.0.0.0, port 5000.
Routes:
    /: Displays 'Hello HBNB!'.
    /hbnb: Displays 'HBNB'.
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    ''' Display "Hello HBNB!" '''
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    ''' Display "HBNB" '''
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    ''' To display c followed by the value of the text variable'''
    text = text.replace("_", " ")
    return ("C {}".format(text))

@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is cool"):
    '''To display Python followed by the value of the text variable
    The default value of text is is cool'''
    text = text.replace("_", " ")
    return ("Python {}".format(text))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
