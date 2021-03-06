# Packages required for current version of the project
from flask import render_template, redirect, request, url_for, session, flash
import requests
from v2.forms import InputForm
from datetime import datetime, timedelta
from v2.article_search import ArticleSearch
from flask import Flask
from v2 import app
from v2.map_test import map_test

# data structure will be used further on for input
intervals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

# data structure will be used further on for input
rates = {
    0: 'Severity Rate',
    1: 'Big Dip',
    2: 'Downtick',
    3: 'Decrease',
    4: 'Flat',
    5: 'Increase',
    6: 'Uptick',
    7: 'Spike',
    8: 'All',
}

# data structure will be used further on for input
check = {
    'period': 1,
    'startDate': 1,
    'endDate': 1,
    'interval': 1,
}

# FUNCTION RUNS WHEN THE BASE HOST IS CALLED WITH THE '/' EXTENTION, e.g. https://localhost:5000/
@app.route("/")
def index():
    inputForm = InputForm() 
    check_return_to_default() # returns all
    return render_template("index.html", form = inputForm, message = '', intervals=intervals, rates=rates, 
                        check=check, filepath='', highlights='', ipt='', start = '', end = '')


# FUNCTION RUNS WHEN THE BASE HOST IS CALLED WITH THE '/map' EXTENTION, e.g. https://localhost:5000/map
# needs to be called with POST API method and data is required when being called
# called within the dashboard after submit button is clicked, cannot be called through the URL without data
@app.route("/map", methods=['GET','POST'])
def map():
    correctInput = True # boolean variable used to check if the input is correct
    inputForm = InputForm()
    message = '' 
    highlights=''


    # called if function called with POST API
    if request.method == "POST":
        ipt = request.form  # put the data into ipt (easier to call the information later in the code), 
                            # format: { allstates: all abbreviations, 'feature1': feature1, 'feature2': feature2}

        periodLength = ipt['periodLength'] # variable contains the period length

        start_of_startDate = ipt['start_of_startDate'] # variable contains start of the base interval inputted by the user 
        
        start_of_endDate = ipt['start_of_endDate'] # variable contains start of the target interval inputted by the user 

        interval = ipt['interval'] # variable contains the type of change to view (Big Dip, Spike, etc.)

        start_of_startDate = datetime.strptime(start_of_startDate, '%Y-%m-%d') # converts the date to an appropriate format
        end_of_startDate = start_of_startDate.date() + timedelta(days=int(periodLength)-1)
                

        start_of_endDate = datetime.strptime(start_of_endDate, '%Y-%m-%d') # converts the date to an appropriate format to be read by the code in map_test.py
        end_of_endDate = start_of_endDate.date() + timedelta(days=int(periodLength)-1)  
	
    articles = ArticleSearch(start_of_endDate.date(), end_of_endDate) # call the ArticleSearch function from article_search.py with the start and end dates of the time interval being checked
    highlights = articles.search() # store the return value of the search() function in article_search.py in highlights

    ##### formatting the 'end_of_startDate' variable to be in appropriate format "%d-%b-%Y"
    end_of_startDate_strip = str(end_of_startDate).split('-') 
    x = datetime(int(end_of_startDate_strip[0]), int(end_of_startDate_strip[1]), int(end_of_startDate_strip[2]))
    end_of_startDate = x.strftime("%d-%b-%Y")

    ##### formatting the 'end_of_endDate' variable to be in appropriate format "%d-%b-%Y"
    end_of_endDate_strip = str(end_of_endDate).split('-')
    x = datetime(int(end_of_endDate_strip[0]), int(end_of_endDate_strip[1]), int(end_of_endDate_strip[2]))
    end_of_endDate = x.strftime("%d-%b-%Y")

    ##### formatting the 'start_of_startDate' variable to be in appropriate format "%d-%b-%Y"
    start_of_startDate_strip = str(start_of_startDate.date()).split('-')
    x = datetime(int(start_of_startDate_strip[0]), int(start_of_startDate_strip[1]), int(start_of_startDate_strip[2]))
    start_of_startDate = x.strftime("%d-%b-%y").upper()

    ##### formatting the 'end_of_endDate' variable to be in appropriate format "%d-%b-%Y"
    start_of_endDate_strip = str(start_of_endDate.date()).split('-')
    x = datetime(int(start_of_endDate_strip[0]), int(start_of_endDate_strip[1]), int(start_of_endDate_strip[2]))
    start_of_endDate = x.strftime("%d-%b-%y").upper()

    # store end dates in readable format
    endDates = {
        'start': end_of_startDate,
        'end': end_of_endDate
    }
    
    gen_map = map_test(periodLength, start_of_startDate, start_of_endDate, interval) # call 'map_test' from map_test.py
    key = gen_map.main() # generate a map using the inputs
    maphash = gen_map.get_maphash() 
    returned_map = maphash[key]
    filepath = "maps/Cases-" + start_of_startDate + "vs" + start_of_endDate + "-intDays" + periodLength + "/" + returned_map # get map url
    check_return_to_default() 

    # load index.html with new url for map
    if endDates['start']:
        return render_template("index.html", form = inputForm, message = message, intervals=intervals, rates=rates, check=check, filepath=filepath, highlights=highlights, ipt=ipt, start = endDates['start'], end=endDates['end'])



# helper function beyond this point
def check_return_to_default():
    check['period'] = 1
    check['startDate'] = 1
    check['endDate'] = 1
    check['interval'] = 1



# api functions beyond this point

if __name__ == "__main__":
    app.run( debug=True)
