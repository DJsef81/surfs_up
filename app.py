# Set Up the Flask Weather App

# We need to create a new Python file and import our dependencies to our code environment.
# The first thing we'll need to import is datetime, NumPy, and Pandas. 
# We assign each of these an alias so we can easily reference them later. 
import datetime as dt
import numpy as np
import pandas as pd

# Now let's get the dependencies we need for SQLAlchemy, which will help us access our data in the SQLite database. 
# Add the SQLAlchemy dependencies after the other dependencies you already imported in app.py.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# This dependency will enable your code to access all that Flask has to offer.
# To import the Flask dependency, add the following to your code:

from flask import Flask, jsonify

# Set Up the Database to access  SQLite 
engine = create_engine("sqlite:///hawaii.sqlite")

# Now let's reflect the database into our classes.
Base = automap_base()

# Add the following code to reflect the database:
Base.prepare(engine, reflect=True)

# With the database reflected, we can save our references to each table.  
# We'll create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database with the following code:
session = Session(engine)

# Create a New Flask App Instance
# "Instance" is a general term in programming to refer to a singular version of something. 
# Set Up Flask
# To define our Flask app, add the following line of code. This will create a Flask application called "app."
app = Flask(__name__)

# Create Flask Routes
# First, we need to define the starting point, also known as the root. 
# We can define the welcome route using the code below:
# All of your routes should go after the app = Flask(__name__) line of code. Otherwise, your code may not run properly.
@app.route('/')

# Now our root, or welcome route, is set up. The next step is to add the routing information for each of the other routes. 
# For this we'll create a function, and our return statement will have f-strings as a reference to all of the other routes. 
# This will ensure our investors know where to go to view the results of our data.

# First, create a function welcome() with a return statement. 
# Next, add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement. 
# We'll use f-strings to display them for our investors:

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <br>
    Available Routes: <br>
    /api/v1.0/precipitation <br>
    /api/v1.0/stations <br>
    /api/v1.0/tobs <br>
    /api/v1.0/temp/start/end <br>
    ''')

# The next route will return the precipitation data for the last year. 
# by building this route we'll be able to access this analysis in real time with just a URL.
@app.route("/api/v1.0/precipitation")

# Next, we will create the precipitation() function.
# add code to the function. 
# Next, write a query to get the date and precipitation for the previous year. 

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Build Stations Route
# Begin by defining the route and route name.
@app.route("/api/v1.0/stations")

# create a new function called stations()
# create a query that will allow us to get all of the stations in our database.
# unravle our results into a one-dimensional array using thefunction np.ravel(), with results as our parameter.
# convert our unraveled results into a list. using the list function, which is list(), and then convert that 
# array into a list. Then we'll jsonify the list and return it as JSON.
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# create the temperature observations route.
@app.route("/api/v1.0/tobs")

# Next, create a function called temp_monthly() by adding the following code:
# calculate the date one year ago from the last date in the database. 
# query the primary station for all the temperature observations from the previous year.
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create Statistics Route
# minimum, maximum, and average temperatures.
# we will have to provide both a starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# create a function called stats() to put our code in.
# Since we need to determine the starting and ending date, add an if-not statement to our code.
# query our database using the list that we just made. 
# unravel the results into a one-dimensional array and convert them to a list. 
# jsonify our results and return them.
# calculate the temperature minimum, average, and maximum with the start and end dates.
#  We'll use the sel list, which is simply the data points we need to collect.

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)