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

intervals = [1, 3, 5, 7, 10, 14]

#####TODO: change to hash table  #########
rates = {
    -1: -1,
    1: 'Big Dip',
    2: 'Downtick',
    3: 'Decrease',
    4: 'Flat',
    5: 'Increase',
    6: 'Uptick',
    7: 'Spike',
    8: 'All',
}
##########################################

check = {
    'period': 1,
    'startDate': 1,
    'endDate': 1,
    'interval': 1,
}

@app.route("/")
def index():
    inputForm = InputForm()
    message = ''
    check_return_to_default()
    return render_template("index.html", form = inputForm, message = message, intervals=intervals, rates=rates, check=check)

@app.route("/map", methods=['GET','POST'])
def map():
    correctInput = True
    inputForm = InputForm()
    message = ''

    if request.method == "POST":
        ipt = request.form
        periodLength = ipt['periodLength']
        start_of_startDate = ipt['start_of_startDate']
        start_of_endDate = ipt['start_of_endDate']
        interval = ipt['interval']
        
        if (int(periodLength) == 1):
            correctInput = False
            check['period'] = 0
        if (start_of_startDate == ''):
            correctInput = False
            check['startDate'] = 0
        if (start_of_endDate == ''):
            correctInput = False 
            check['endDate'] = 0
        if (int(interval) == -1):
            correctInput = False
            check['interval'] = 0
        
        if not correctInput:
            message = "Empty Fields"
            return render_template("index.html", form = inputForm, message = message, intervals=intervals, rates=rates, check=check)

        start_of_startDate = datetime.strptime(start_of_startDate, '%Y-%m-%d')
        end_of_startDate = start_of_startDate.date() + timedelta(days=int(periodLength)-1)

        start_of_endDate = datetime.strptime(start_of_endDate, '%Y-%m-%d')
        end_of_endDate = start_of_endDate.date() + timedelta(days=int(periodLength)-1)

        if end_of_startDate > start_of_endDate.date():
            message = 'Periods cannot overlap!'
            check['endDate'] = 0
            check['startDate'] = 0
            return render_template("index.html", form = inputForm, message = message, intervals=intervals, rates=rates, check=check)
            
            ###########TODO: create sync with Endrit's code##################
            
    start_of_startDate_strip = str(start_of_startDate.date()).split('-')
    x = datetime(int(start_of_startDate_strip[0]), int(start_of_startDate_strip[1]), int(start_of_startDate_strip[2]))
    start_of_startDate = x.strftime("%d-%b-%y").upper()

    start_of_endDate_strip = str(start_of_endDate.date()).split('-')
    x = datetime(int(start_of_endDate_strip[0]), int(start_of_endDate_strip[1]), int(start_of_endDate_strip[2]))
    start_of_endDate = x.strftime("%d-%b-%y").upper()
    
    gen_map = map_test.map_test(periodLength, start_of_startDate, start_of_endDate, interval)
    key = gen_map.main()
    print(key)

            ##################################################################
        
    check_return_to_default()
    return render_template("index.html", form = inputForm, message = message, intervals=intervals, rates=rates, check=check, correctInput=correctInput)




# helper function beyond this point
def check_return_to_default():
    check['period'] = 1
    check['startDate'] = 1
    check['endDate'] = 1
    check['interval'] = 1



# api functions beyond this point
    

if __name__ == "__main__":
    app.run(debug=True)
    

