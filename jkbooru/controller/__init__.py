# -*- coding: utf-8 -*-
from jkbooru import app


@app.route("/")
def hello():
    return "Hello World!"
