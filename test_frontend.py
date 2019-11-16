import requests
import json
import pytest
import frontend
from frontend import app
import sys

"""
Test GET and POST functionality
for both endpoints
"""


def test_APIs(u, p):
    session = requests.Session()
    session.auth = (u, p)

    x = session.post(
        "http://0.0.0.0:5000/location/api/delivery/delivery_location",
        data={"latitude": 9, "longitude": 8},
    )
    json_request = json.loads(x.content)
    assert isinstance(json_request[0]["latitude"], float)
    assert isinstance(json_request[0]["longitude"], float)

    x = session.get("http://0.0.0.0:5000/location/api/delivery/delivery_location")
    json_request = json.loads(x.content)
    assert isinstance(json_request[0]["latitude"], float)
    assert isinstance(json_request[0]["longitude"], float)

    x = session.post(
        "http://0.0.0.0:5000/location/api/delivery/robot_location",
        data={"latitude": 9, "longitude": 8},
    )
    json_request = json.loads(x.content)
    assert isinstance(json_request[0]["latitude"], float)
    assert isinstance(json_request[0]["longitude"], float)

    x = session.get("http://0.0.0.0:5000/location/api/delivery/robot_location")
    json_request = json.loads(x.content)
    assert isinstance(json_request[0]["latitude"], float)
    assert isinstance(json_request[0]["longitude"], float)


"""
Test DB 
"""


def test_DB():
    with app.app_context():
        frontend.init_db()
        frontend.insert_into_db(
            "INSERT INTO robot_location (del_id, time, latitude, longitude) VALUES (0,0,0,0)"
        )
        result = frontend.query_db("select * from robot_location where del_id = 0")
        result_fail = frontend.query_db(
            "select * from robot_location where del_id = -1"
        )
    assert result != []
    assert result_fail == []
