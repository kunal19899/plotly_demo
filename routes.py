from flask import render_template, Flask, redirect, request, url_for, session, flash
import requests
from flask import Flask
from config import Config

app = Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object(Config)

@app.route("/")
def index():
    return render_template("index.html", index=True)

@app.route('/get_map')
def get_map():
    return render_template('map.html', get_map = True)
    

if __name__ == "__main__":
    app.run(debug=True)