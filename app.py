from flask import Flask, render_template

app =Flask(__name__)



@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/about")
def aboutpage():
   return render_template("about.html")

@app.route("/flashcards")
def flashpage():
    return "Here are youre Flashcards"


