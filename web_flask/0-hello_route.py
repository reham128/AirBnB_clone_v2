#!/usr/bin/python3
"""a script that starts a Flask web application"""
from flask import Flask
from werkzeug.utils import url_quote

app = Flask(__name__)
"""flask app instance"""


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """/: display “Hello HBNB!”"""
    return ('Hello HBNB!')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
