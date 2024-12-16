# Import the dependencies
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify, abort
from datetime import datetime, timedelta

#################################################
# Database Setup
#################################################

# Create engine and reflect an existing database into a new model
Base = automap_base()
engine = create_engine('sqlite:///C:\\Users\\Jakeu\\Desktop\\Data Bootcamp\\Module Challenge\\Module_10\\sqlalchemy-challenge\\Resources\\hawaii.sqlite')
Base.prepare(autoload_with=engine)  # Use autoload_with to avoid deprecation warning

# Reflect tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Save references to each table
tables = {table_name: getattr(Base.classes, table_name) for table_name in Base.classes.keys()}

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    """List all available routes."""
    return (
        f"Welcome to the Climate API!<br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/&lt;start&gt;<br>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    """Return the last 12 months of precipitation data as JSON."""
    # Find the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = datetime.strptime(most_recent_date, '%Y-%m-%d')

    # Calculate the date one year back
    start_date = most_recent_date - timedelta(days=365)

    # Query precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= start_date,
        Measurement.prcp != None
    ).all()

    # Convert to dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    """Return a list of stations as JSON."""
    # Query distinct stations
    results = session.query(Station.station).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    """Return the last 12 months of temperature observations for the most active station."""
    # Find the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = datetime.strptime(most_recent_date, '%Y-%m-%d')

    # Calculate start date (1 year back)
    start_date = most_recent_date - timedelta(days=365)

    # Find the most active station
    most_active_station = session.query(
        Measurement.station, func.count(Measurement.station)
    ).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]

    # Query temperature observations for the most active station
    results = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.station == most_active_station,
        Measurement.date >= start_date
    ).all()

    # Convert to list
    temperature_data = [tobs for date, tobs in results]
    return jsonify(temperature_data)

@app.route('/api/v1.0/<start>')
def start_date_only(start):
    """Return TMIN, TAVG, and TMAX for dates greater than or equal to the start date."""
    try:
        # Parse start date
        start_date = datetime.strptime(start, '%Y-%m-%d')
    except ValueError:
        abort(400, description="Invalid date format. Please use YYYY-MM-DD format.")

    # Query temperature stats
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start_date).all()

    temperature_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    return jsonify(temperature_stats)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    """Return TMIN, TAVG, and TMAX for dates between the start and end dates inclusive."""
    try:
        # Parse start and end dates
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        abort(400, description="Invalid date format. Please use YYYY-MM-DD format.")

    # Query temperature stats
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    temperature_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    return jsonify(temperature_stats)

if __name__ == '__main__':
    app.run(debug=True)
