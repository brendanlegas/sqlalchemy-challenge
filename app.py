import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
        session = Session(engine)
        date = dt.datetime(2016, 8, 22)
        sel = [measurement.date, measurement.prcp]
        last_12_months = session.query(*sel).filter(measurement.date>date).all()

        return jsonify(last_12_months)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(station.station).all()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    date = dt.datetime(2016, 8, 22)
    tobs = session.query(measurement.tobs, measurement.date).filter(measurement.date>date).filter(measurement.station == "USC00519281").all()

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def calculations(start_date):
    session = Session(engine)
    start_date = dt.datetime(start_date)
    sel = [measurement.station,
       func.min(measurement.tobs),
       func.max(measurement.tobs),
       func.avg(measurement.tobs)]
    calculated = session.query(*sel).filter(measurement.date > start_date).all()

    return jsonify(calculated)

if __name__ == "__main__":
    app.run(debug=False)