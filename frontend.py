##################
# Imports
##################
import sqlite3
from sqlite3 import OperationalError
import pytest
import datetime
from user import User
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash,generate_password_hash
from flask import Flask, render_template, url_for, jsonify, request, abort, g, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user




##########################
# Flask Global Variables #
##########################
app = Flask(__name__)
DATABASE = "../instance/GUADR.db"
auth = HTTPBasicAuth()
#set the secret key
app.secret_key = "secret"

###############
# Login specs #   
###############
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


#############################
# Mapping and API Variables # 
#############################
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
delivery_locations = [
    "Foley Library",
    "Hemmingson NW Corner",
    "Herak NE Corner",
    "Crosby North Entrance",
]
latitudes_list = [latitude_robot, latitude_destination]
longitudes_list = [longitude_robot, longitude_destination]


##################
#   ROUTES       #
##################
@app.route("/")
def base():
    return redirect(url_for('login'))

#signup
@app.route("/signup", methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        username = request.form.get('UserN')
        password = request.form.get('UserP')
        passcheck = request.form.get('UserP2')

        #check to see if password is longer than 8 characters
        pass_short = False
        if password is None or len(password) < 8:
            pass_short = True

        #check to see if the password entries match
        pass_mismatch = False
        if password != passcheck:
            pass_mismatch = True


        #check to see if the user exists in the system,
        all_users = query_db("select * from users")
        username_taken = False
        for x in all_users:
            if username == x['username']:
                username_taken = True

        #if username is taken
        if pass_mismatch:
            flash("Password entries don't match")
            return render_template("signup.html")
        elif username_taken:
            flash("Username is already taken")
            return render_template("signup.html")
        elif pass_short:
            flash("Password must be at least 8 characters long")
            return render_template("signup.html")
        elif username is None or password is None:
            return render_template("signup.html")
        else:
            #if successfully made account
            next_id = len(all_users) + 1
            insert_into_db("insert into users (username,password) values (?,?)",
                    (username,
                    generate_password_hash(password)
                        ))
            return redirect(url_for("login"))
    else:
        return render_template("signup.html")



@app.route("/login", methods=['GET','POST'])
def login():
    #Get username and password from the form
    username = request.form.get('UserN')
    password = request.form.get('UserP')

    #get all users to check against
    all_users = query_db("select * from users")
    successful_login = False

    #Iterate through all users and check if its the correct information
    for x in all_users:
        if username == x['username'] and check_password_hash(x['password'],password):
            #create user for login, login them in and check if vender or user
            user = User(x['id'],x['username'],x['password'])
            login_user(user)
            if x['vender'] == 1:
                return redirect(url_for('vender'))
            return redirect(url_for('home'))
    
    #Check for incorrect login
    if username is not  None and password is not  None:
        flash("Incorrect Login Credentials")

    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/vender', methods=['GET','POST'])
@login_required
def vender():
    #get the entered food name and price
    food_name = request.form.get('foodName')
    food_price = request.form.get('foodPrice')

    #Add the food to the venders items
    if food_name is not None and food_price is not None:
        food_price = float(food_price)
        food_price = "{:.2f}".format(food_price)


        #Get the vender id
        all_food = query_db("select * from vender where id = ?",(str(current_user.id)))
        
        #Check if food item already in
        should_add = True
        for food in all_food:
            if food['food_item']== food_name:
                should_add = False

        #if not, insert it
        if should_add:
            insert_into_db("Insert into vender(id,food_item,food_price) values (?,?,?)",
               (
                str(current_user.id),
                food_name,
                food_price
                   ))

    #update food list
    all_food = query_db("select * from vender where id = ?",(str(current_user.id)))
    for food_item in all_food:
        food_item['food_price'] =  float(food_item['food_price']) 
        food_item['food_price'] =  "{:.2f}".format( food_item['food_price'] )

    return render_template(
            'vender.html',
            name=current_user.username,
            vendor_id = current_user.id,
            currentOfferings = all_food,
            )


@app.route("/home", methods=["GET","POST"])
@login_required
def home():

    chosen_food=0 
    all_stores = query_db("select username from users where vender = 1")

    if request.method == 'POST':

        for store in all_stores:
            if request.form['store_buttons'] == store['username']:
                chosen_store = store['username']

        if chosen_store is not None:
            chosen_store_id = query_db("select id from users where username = ?", (chosen_store,))
            chosen_food = query_db("select food_item from vender where id = ?", (chosen_store_id[0]['id'],)) 

    return render_template(
        "home.html",
        title="GUADR Mockup",
        foods=chosen_food,
        stores = all_stores,
        locations=delivery_locations,
        cur_per=current_percentage,
        rem_time=remaining_time,
        loc_url=location_url,
        name=current_user.username,
    )


#################
# Login Manager #
#################
@login_manager.user_loader
def load_user(user_id):
    curr_user = query_db("select * from users where id = (?)", (user_id,))
    user = User(curr_user[0]['id'],curr_user[0]['username'],curr_user[0]['password'])
    return user


##############
#   API      #
##############
@app.route("/location/api/delivery/robot_location", methods=["GET", "POST"])
@login_required
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
@login_required
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
                "del_loc": str(request.form["del_loc"]),
                "food_items": str(request.form["food_items"])

            }
        ]

        insert_into_db(
            "INSERT INTO delivery_location ( latitude, longitude, del_loc, food_items) VALUES (?, ?,?,?)",
            (float(request.form["latitude"]), float(request.form["longitude"]), request.form["del_loc"], str(request.form["food_items"])),
        )
        return jsonify(delivery), 201
    else:
        abort(404)


@app.route("/location/api/delivery/route", methods=["GET"])
@login_required
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
    Connect to the db and 
    return the db connection
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
        already_substantiated = query_db("select name from sqlite_master where type='table' and name='users'") 
        if already_substantiated == []:
            with app.open_resource("schema.sql", mode="r") as f:
                db.cursor().executescript(f.read())
            db.commit()

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0")
