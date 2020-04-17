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
def test_redirect_home_to_login():
    session = requests.Session()
    session.auth = ("reid", "reidreid")
    x = session.get("http://guadr.gonzaga.edu/home")
    assert str(x.url[20:25] == 'login')

def test_login():
    session = requests.Session()
    session.auth = ("reid", "reidreid")
    x = session.get("http://guadr.gonzaga.edu/login")
    assert x.status_code == 200

def test_signup():
    session = requests.Session()
    session.auth = ("reid", "reidreid")
    x = session.get("http://guadr.gonzaga.edu/signup")
    assert x.status_code == 200

def test_vendor():
    session = requests.Session()
    session.auth = ("reid", "reidreid")
    x = session.get("http://guadr.gonzaga.edu/vender")
    assert x.status_code == 200

  

"""
Test DB 
"""
def test_DB():
    with app.app_context():
        frontend.init_db()
        frontend.insert_into_db(
            "INSERT INTO robot_location (del_id, time, latitude, longitude,perc_complete) VALUES (0,0,0,0,0.0)"
        )
        result = frontend.query_db("select * from robot_location where del_id = 0")
        result_fail = frontend.query_db(
            "select * from robot_location where del_id = -1"
        )
    assert result != []
    assert result_fail == []
