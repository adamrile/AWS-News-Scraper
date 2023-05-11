**Football API Data Ingestion**

This repository contains a Python script to connect to a football API and return a summary of the number of teams in each competition. The data is fetched from the API, processed, and stored into a database, and a summary CSV file is generated as output.

_Features_

Connects to the football API and fetches competition and team data
Inserts competition and team data into a database
Generates a summary CSV file containing the number of teams in each competition

_Requirements_

Python 3.6 or later
requests library
PostgreSQL database

_Installation_

1. Clone the repository:

- git clone https://github.com/yourusername/football-api-data-ingestion.git
- cd football-api-data-ingestion

2. Install the required packages:

- pip install -r requirements.txt

3. Set up the PostgreSQL database and configure the connection details in create_tables.py file

_Usage_

To run the script, execute the following commands in your terminal:

- python3 create_tables.py
- python3 main.py

The script reset the database and will fetch data from the API, insert it into the database, and generate a summary CSV file named summary.csv in the ./output directory.

To run the tests, execute the following command in your terminal:

- python3 tests.py

_Files_

main.py: The main script that connects to the football API, fetches competition and team data, and processes it.

create_tables.py: Contains the get_db_connection() function to set up a connection to the PostgreSQL database.

_Functions_

ingest_comp_data(url: str, headers: str = None) -> list: Fetches competition data from the API and returns it in JSON format along with a list of competition codes.

ingest_team_data(url: str, headers: str = None) -> list: Fetches team data from the API using the provided team URL and returns it in JSON format.

insert_comp_data(comp_data: list) -> str: Inserts competition data into the dims_competition table in the database.

insert_team_data(team_data: list, comp_id: list) -> str: Inserts team data into the dim_teams and fact_competitions tables in the database.

output_summary_csv(): Generates a summary CSV file containing the number of teams in each competition.
