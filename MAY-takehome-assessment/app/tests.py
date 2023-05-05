import pytest
import os
import csv
import requests_mock
from main import ingest_comp_data, ingest_team_data, output_summary_csv, insert_comp_data, insert_team_data, get_db_connection

@pytest.fixture
def mock_req():
    with requests_mock.Mocker() as m:
        yield m

def test_ingest_comp_data(mock_req):
    url = 'https://api.football-data.org/v4/competitions'
    mock_data = {
        "competitions": [
            {"code": "TEST", "id": 1, "name": "Test Competition"}
        ]
    }
    mock_req.get(url, json=mock_data)

    codes, data = ingest_comp_data(url)
    assert codes == ["TEST"]
    assert data == mock_data

def test_ingest_team_data(mock_req):
    url = 'http://api.football-data.org/v4/competitions/TEST/teams'
    mock_data = {
        "teams": [
            {"id": 1, "name": "Test Team"}
        ]
    }
    mock_req.get(url, json=mock_data)

    data = ingest_team_data(url)
    assert data == mock_data


def test_ingest_comp_data():
    url = 'https://api.football-data.org/v4/competitions'
    headers = {'X-Auth-Token': '041904737e094e1f9b765fb9ba79d905'}
    competition_code, comp_data = ingest_comp_data(url, headers=headers)
    assert isinstance(competition_code, list)
    assert isinstance(comp_data, dict)

def test_insert_comp_data():
    comp_data = {'competitions': [{'id': 2021, 'name': 'Premier League'}, {'id': 2002, 'name': 'Bundesliga'}]}
    insert_comp_data(comp_data)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM dim_competitions")
    result = cur.fetchone()[0]
    assert result == 2
    cur.close()
    conn.close()

def test_insert_team_data():
    team_data = {'teams': [{'id': 57, 'name': 'Arsenal'}, {'id': 61, 'name': 'Chelsea'}]}
    comp_id = 2021
    insert_team_data(team_data, comp_id)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM dim_teams")
    result = cur.fetchone()[0]
    assert result == 2
    cur.execute("SELECT COUNT(*) FROM fact_competitions")
    result = cur.fetchone()[0]
    assert result == 2
    cur.close()
    conn.close()

def test_output_summary_csv():
    output_summary_csv()
    output_file = os.path.join('./output', 'summary.csv')
    with open(output_file, 'r') as file:
        reader = csv.reader(file)
        assert next(reader) == ['Competition', 'Number of Teams']
        assert next(reader) == ['Premier League', '20']
        assert next(reader) == ['Bundesliga', '0']
