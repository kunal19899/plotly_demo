from flask import render_template, Flask, redirect, request, url_for, session, flash
import requests
from flask import Flask
from config import Config
from forms import InputForm

app = Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object(Config)

@app.route("/")
def index():
    inputForm = InputForm()
    return render_template("index.html", index=True, form = inputForm)



# helper function beyond this point


# api functions beyond this point
    

if __name__ == "__main__":
    app.run(debug=True)
