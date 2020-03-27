import sqlite3
import datetime
from flask import Flask, render_template, url_for, jsonify, request, abort, g, redirect, flash
import pytest
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import LoginManager


"""
authorization using https://github.com/miguelgrinberg/Flask-HTTPAuth
"""
DATABASE = "../instance/GUADR.db"
app = Flask(__name__)
auth = HTTPBasicAuth()

#login_manager = LoginManager()
#login_manager.init_app(app)

#set the secret key
#####REMOVE BEFORE PUSh#
app.secret_key='lookatallthosechickens'

# Set Variables
current_percentage = 0.0
remaining_time = 0 
latitude_robot = 47.667560
longitude_robot = -117.401629
latitude_destination = 47.666867
longitude_destination = -117.401701
lat_offset = 0.000633
long_offset = 0.000755
default_layer = "hot"
hc_location_url = "https://www.openstreetmap.org/?mlat=47.66753&mlon=-117.40291#map=18/47.66753/-117.40291"
location_url = (
    "https://www.openstreetmap.org/export/embed.html?bbox="
    + (str(longitude_destination - long_offset))
    + "%2C"
    + (str(latitude_destination - lat_offset))
    + "%2C"
    + (str(longitude_destination + long_offset))
    + "%2C"
    + (str(latitude_destination + lat_offset))
    + "&layer="
    + default_layer
    + "&marker="
    + (str(latitude_destination))
    + "%2C"
    + (str(longitude_destination))
)
food_items = ["Sandwich", "Soda", "Candy", "Trail Mix", "Beef Jerky", "Muffin", "La Croix", "Bang Energy Drink", "Redbull 16oz", "Eggs", "Bacon", "Pancakes"]
delivery_locations = [
    "Foley Library",
    "Hemmingson NW Corner",
    "Herak NE Corner",
    "Crosby North Entrance",
]
latitudes_list = [latitude_robot, latitude_destination]
longitudes_list = [longitude_robot, longitude_destination]


@auth.verify_password
def verify_password(username, password):
    base_user = query_db("select * from users", one=True)
    if username == base_user["username"] and check_password_hash(
        base_user["password"], password
    ):
        return True
    return False

@app.route("/")
def base():
    return redirect(url_for('login'))

#signup
@app.route("/signup", methods=['GET','POST'])
def signup():
    username = request.form.get('UserN')
    password = request.form.get('UserP')

    #check to see if the user exists in the system,
    #if user exists
        #render signup
    #else 
        #create new user
        #add new user to db
        #redirect to login

    all_users = query_db("select * from users")
    username_taken = False
    for x in all_users:
        if username == x['username']:
            username_taken = True

    print(username_taken)
    
    if username_taken:
        flash("Username is taken")
        return render_template("signup.html")
    elif username is None or password is None:
        flash("You must enter a username and password")
        return render_template("signup.html")
    else:
        next_id = len(all_users) + 1
        insert_into_db("insert into users (username,password) values ('" + username + "','" + generate_password_hash(password) + "')")
        return redirect(url_for("login"))

#login
@app.route("/login", methods=['GET','POST'])
def login():
    return render_template("login.html")


# Home Route
@app.route("/home")
@auth.login_required
def hello():
    return render_template(
        "home.html",
        title="GUADR Mockup",
        foods=food_items,
        locations=delivery_locations,
        cur_per=current_percentage,
        rem_time=remaining_time,
        loc_url=location_url,
    )


##############
#   API      #
##############
@app.route("/location/api/delivery/robot_location", methods=["GET", "POST"])
@auth.login_required
def get_robot_location():
    if request.method == "GET":
        """
        If GET, get the latitude and longitude
        of the latest robot location 
        """
        loc = query_db(
            """select latitude, longitude, perc_complete 
                           from robot_location 
                           where time = (select MAX(time)  
                                         from robot_location) """
        )

        return jsonify(loc)

    elif request.method == "POST":
        """
        If POST, get the latest delivery_id (the one that we are on, 
        since we are only handling one user), and insert the updated
        location
        """
        robot_loc = [
            {
                "latitude": float(request.form["latitude"]),
                "longitude": float(request.form["longitude"]),
                "perc_complete": float(request.form["perc_complete"])
            }
        ]

        max_del = query_db(
            "SELECT max(delivery_id) as id FROM delivery_location", one=True
        )

        insert_into_db(
            "INSERT INTO robot_location (del_id, time, latitude, longitude, perc_complete) VALUES (?,?,?,?,?)",
            (
                max_del["id"],
                datetime.datetime.now(),
                float(request.form["latitude"]),
                float(request.form["longitude"]),
                float(request.form["perc_complete"])
            ),
        )
        return jsonify(robot_loc), 201

    else:
        abort(404)


@app.route("/location/api/delivery/delivery_location", methods=["GET", "POST"])
@auth.login_required
def get_delivery_location():
    if request.method == "GET":
        """
        If GET: get the latest
        long and lat to respond
        """
        loc = query_db(
            """select latitude, longitude 
                        from delivery_location 
                        where delivery_id = (select MAX(delivery_id) 
                                                   from delivery_location)"""
        )
        return jsonify(loc)

    elif request.method == "POST":
        """
        IF post, get the given location
        and update the DB.
        """
        delivery = [
            {
                "latitude": float(request.form["latitude"]),
                "longitude": float(request.form["longitude"]),
            }
        ]

        insert_into_db(
            "INSERT INTO delivery_location ( latitude, longitude) VALUES (?, ?)",
            (float(request.form["latitude"]), float(request.form["longitude"])),
        )
        return jsonify(delivery), 201
    else:
        abort(404)

@app.route("/location/api/delivery/route", methods=["GET"])
@auth.login_required
def route():
    if request.method == "GET":
        """
        If Get: reply the route
        """
        route = []
        with open("paths/SW-Hem_Herak.txt") as pathfile:
            for line in pathfile:
                x = (line.strip("\n"))
                coordinate = tuple(x.split(','))
                route.append(coordinate)
        return jsonify(route),201
    else:
        abort(404)


"""
Database: Code adopted from https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
"""


def get_db():
    """
    Connect to the dband 
    returns the db connection
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts  # Make the module return dictionaries
    return db


def make_dicts(cursor, row):
    """
    Make a dictioanry with the given
    cursor and rows
    """
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


@app.teardown_appcontext
def close_connection(exception):
    """
    Close DB connection
    """
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def insert_into_db(query, args=()):
    """
    pass in query and arguments to 
    execute and commit changes
    on databse.
    """
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    cur.close()


def query_db(query, args=(), one=False):
    """
    Replies a dictionary holding
    the response from query.
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def init_db():
    """
    Initialize the databse with the given schema.
    """
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == "__main__":
    #init_db()
    app.run(host="0.0.0.0")
