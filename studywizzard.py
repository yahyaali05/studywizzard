from flask import Flask, render_template

studywizzard =Flask(__name__)



@studywizzard.route("/")
def homepage():
    return render_template("homepage.html")


@studywizzard.route("/about")
def aboutpage():
   return render_template("about.html")

@studywizzard.route("/flashcards")
def flashpage():
    return "Here are youre Flashcards"


