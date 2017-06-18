from flask import render_template, request

from bookish.app import app
from bookish.util.randomizer import pick_one
from bookish.util.loader import all_translations
from bookish.util.validator import validate


@app.route("/")
def root():
    return render_template("main.html", translation=pick_one(all_translations()), evaluation=validate(request.args))
