Jupyter Notebook Database Connection
Used the SQLAlchemy create_engine() function to connect to your SQLite database.
Used the SQLAlchemy automap_base() function to reflect your tables into classes.
Saved references to the classes named station and measurement.
Linked Python to the database by creating a SQLAlchemy session.
Closed your session at the end of your notebook.
Precipitation Analysis
Created a query that found the most recent date in the dataset (8/23/2017).
Created a query that collected only the date and precipitation for the last year of data without passing the date as a variable.
Saved the query results to a Pandas DataFrame with date and precipitation columns.
Sorted the DataFrame by date.
Plotted the results by using the DataFrame plot method with date as the x and precipitation as the y variables.
Used Pandas to print the summary statistics for the precipitation data.
Station Analysis
Designed a query that found the number of stations in the dataset (9).
Designed a query that listed the stations and observation counts in descending order and identified the most active station (USC00519281).
Designed a query that found the min, max, and average temperatures for the most active station (USC00519281).
Designed a query to retrieve the previous 12 months of temperature observation (TOBS) data filtered by the station with the greatest number of observations.
Saved the query results to a Pandas DataFrame.
Correctly plotted a histogram with bins=12 for the last year of data using tobs as the column to count.
API SQLite Connection & Landing Page
Correctly generated the engine to the correct SQLite file.
Used automap_base() and reflected the database schema.
Saved references to the tables in the SQLite file (measurement and station).
Created and bound the session between the Python app and the database.
Displayed the available routes on the landing page.
API Static Routes
A precipitation route that:

Returned JSON with the date as the key and the value as the precipitation.
Only returned the JSONified precipitation data for the last year in the database.
A stations route that:

Returned JSONified data of all the stations in the database.
A tobs route that:

Returned JSONified data for the most active station (USC00519281).
Only returned the JSONified data for the last year of data.
API Dynamic Route
A start route that:

Accepted the start date as a parameter from the URL.
Returned the min, max, and average temperatures calculated from the given start date to the end of the dataset.
A start/end route that:

Accepted the start and end dates as parameters from the URL.
Returned the min, max, and average temperatures calculated from the given start date to the given end date.
Coding Conventions and Formatting
Placed imports at the top of the file, just after any module comments and docstrings, and before module globals and constants.
Named functions and variables with lowercase characters, with words separated by underscores.
Followed DRY (Don't Repeat Yourself) principles, creating maintainable and reusable code.
Used concise logic and creative engineering where possible.
