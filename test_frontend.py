import requests
import json
import pytest
import frontend
from frontend import app

'''
Test GET and POST functionality
for both endpoints
'''
def test_delivery_POST():
    x = requests.post('http://guadr.com/location/api/delivery/delivery_location', data={"latitude": 9, "longitude": 8})
    json_request = json.loads(x.content)
    assert (isinstance(json_request[0]['latitude'], float) and ( isinstance(json_request[0]['longitude'], float))) 

def test_delivery_GET():
    x = requests.get('http://guadr.com/location/api/delivery/delivery_location')
    json_request = json.loads(x.content)
    assert (isinstance(json_request[0]['latitude'], float) and ( isinstance(json_request[0]['longitude'], float))) 

def test_robot_POST():
    x = requests.post('http://guadr.com/location/api/delivery/robot_location', data={"latitude": 9, "longitude": 8})
    json_request = json.loads(x.content)
    assert (isinstance(json_request[0]['latitude'], float) and ( isinstance(json_request[0]['longitude'], float))) 

def test_robot_GET():
    x = requests.get('http://guadr.com/location/api/delivery/robot_location')
    json_request = json.loads(x.content)
    assert (isinstance(json_request[0]['latitude'], float) and ( isinstance(json_request[0]['longitude'], float))) 

'''
Test DB 
'''
def test_DB():
    with app.app_context():
        frontend.init_db()
        frontend.insert_into_db('INSERT INTO robot_location (del_id, time, latitude, longitude) VALUES (0,0,0,0)')
        result = frontend.query_db('select * from robot_location where del_id = 0')
        result_fail = frontend.query_db('select * from robot_location where del_id = -1')
    assert result != []
    assert result_fail == []
