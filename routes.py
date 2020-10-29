from flask import render_template, Flask, redirect, request, url_for, session, flash
import requests
from flask import Flask
from config import Config
from forms import InputForm
from maptest import map_test
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object(Config)

@app.route("/")
def index():
    inputForm = InputForm()
    message = ''
    return render_template("index.html", form = inputForm, message = message)

@app.route("/map", methods=['GET','POST'])
def map():
    correctInput = False
    inputForm = InputForm()
    message = ''

    if request.method == "POST":
        ipt = request.form
        periodLength = ipt['periodLength']
        if periodLength == "Select a Period Length": periodLength = -1


        start_of_startDate = ipt['start_of_startDate']
        start_of_startDate = datetime.strptime(start_of_startDate, '%Y-%m-%d')
        start_of_endDate = start_of_startDate.date() + timedelta(days=int(periodLength))


        start_of_endDate = ipt['start_of_endDate']
        start_of_endDate = datetime.strptime(start_of_endDate, '%Y-%m-%d')
        end_of_endDate = start_of_endDate.date() + timedelta(days=int(periodLength))
        interval = ipt['interval']
        if interval == "% Interval": interval = -1
        
        if (periodLength != -1) and (start_of_startDate != '') and (start_of_endDate != '') and (interval != -1):
            correctInput = True
            
            ###########TODO: create sync with Endrit's code##################
            
            # map_test.main()


            ##################################################################
    if not correctInput:
        message = "All Fields must be non-empty!"

        return render_template("index.html", form = inputForm, message = message)

    # call function for plotly here - returns 
    

    return render_template("index.html", form = inputForm, message = message)




# helper function beyond this point


# api functions beyond this point
    

if __name__ == "__main__":
    app.run(debug=True)
    curr_input = {}
