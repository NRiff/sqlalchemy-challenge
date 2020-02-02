#importing and setting up sqlalchemy engine/setting up Flask
import numpy as np
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

start_date= dt.date (2016, 12, 23)
end_date= dt.date (2016,12, 25)

app = Flask(__name__)

# Creating Home page with list of routes
@app.route("/")
def home():
    return (
        f"Welcome to the Home Page<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        )
# route paths for each route from home page
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").group_by(Measurement.date).all()
    print(results)
    session.close()
    
    percpt_api = list(np.ravel(results))
    print(percpt)
    return jsonify(percpt_api)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.name).all()
    Station_api = list(np.ravel(results))
    return jsonify(Station_api)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()
    tobs_api = list(np.ravel(results))
    return jsonify(tobs_api)

@app.route("/api/v1.0/start")
def begining_date():
    session = Session(engine)

    min_results = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    max_results = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    avg_results = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    start_api_min = list(np.ravel(min_results))
    start_api_max= list(np.ravel(max_results))
    start_api_avg= list(np.ravel(avg_results))
    return jsonify(start_api, start_api_max, start_api_avg)

@app.route("/api/v1.0/start/end")
def beetween_date():
    session = Session(engine)

    min_results = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    max_results = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    avg_results = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
    start_api_min = list(np.ravel(min_results))
    start_api_max= list(np.ravel(max_results))
    start_api_avg= list(np.ravel(avg_results))
    return jsonify(start_api, start_api_max, start_api_avg)

if __name__ == "__main__":
    app.run(debug=True)