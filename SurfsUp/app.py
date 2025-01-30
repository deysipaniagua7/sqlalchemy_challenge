# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Part 2: Design Your Climate App

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/2016-08-23<br/>" #edit
        f"/api/v1.0/start/2016-08-23/end/2017-08-23<br/>" #edit
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all results from precipitation analysis"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    session.close()

# Create a dictionary from the row data and append to a list of all precipitation
    all_rain = []

    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_rain.append(precipitation_dict)

    return jsonify(all_rain)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of tobs data over the last 12 months for most active station"""
    # Query tobs over the last 12 months for most active station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-23", Measurement.station == 'USC00519281' ).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    session.close()

# Create a dictionary from the row data and append to a list of tobs
    all_tobs = []
    
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)


# Return a JSON list of the minimum temperature, the average temperature,and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
@app.route("/api/v1.0/start/2016-08-23")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of TMIN, TAVG, TMAX for dates >=2016-08-23"""
    # Query all stats for dates >=2016-08-23
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= "2016-08-23").all()
    
    session.close()

# Create a dictionary from the row data and append to a list of all stats for dates >=2016-08-23
    all_start = []

    for min, avg, max in results:
        start_dict = {}
        start_dict["min_temp"] = min
        start_dict["avg_temp"] = avg
        start_dict["max_temp"] = max
        all_start.append(start_dict)

    return jsonify(all_start)
    

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/start/2016-08-23/end/2017-08-23")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of TMIN, TAVG, TMAX for dates >= 2016-08-23 AND <= 2017-08-23"""
    # Query all stats for dates >= 2016-08-23 AND <= 2017-08-23
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.date <= "2017-08-23").all()
    
    session.close()

# Create a dictionary from the row data and append to a list of all stats for dates >= 2016-08-23 AND <= 2017-08-23.
    all_start_end = []

    for min, avg, max in results:
        start_end_dict = {}
        start_end_dict["min_temp"] = min
        start_end_dict["avg_temp"] = avg
        start_end_dict["max_temp"] = max
        all_start_end.append(start_end_dict)

    return jsonify(all_start_end)


if __name__ == '__main__':
    app.run(debug=True)
