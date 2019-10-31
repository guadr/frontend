from flask import Flask, render_template, url_for, jsonify, request, abort
app = Flask(__name__)

current_percentage = 30
remaining_time = 100
latitude_robot = 47.667560
longitude_robot = -117.401629
latitude_destination = 47.666867
longitude_destination = -117.401701
lat_offset = 0.000633
long_offset = 0.000755
default_layer = "hot"
hc_location_url = "https://www.openstreetmap.org/?mlat=47.66753&mlon=-117.40291#map=18/47.66753/-117.40291"
location_url = "https://www.openstreetmap.org/export/embed.html?bbox=" + (str(longitude_destination - long_offset)) + "%2C" + (str(latitude_destination - lat_offset)) + "%2C" + (str(longitude_destination + long_offset)) + "%2C" + (str(latitude_destination + lat_offset)) + "&layer=" + default_layer + "&marker=" + (str(latitude_destination)) + "%2C" + (str(longitude_destination))

food_items = ["Sandwich","Soda","Candy","Trail Mix","Beef Jerky","Muffin"]
delivery_locations = ["Foley Library", "Hemmingson NW Corner", "Herak NE Corner", "Crosby North Entrance"]
latitudes_list = [latitude_robot, latitude_destination]
longitudes_list = [longitude_robot, longitude_destination]

#For API
delivery = {
        'Delivery_Location': [47.666867, -117.4017010], 
        'Robot_Location': [47.666867, -117.4017010]
        }


@app.route("/")
def hello():
    return render_template("home.html", title="GUADR Mockup" , foods=food_items, locations=delivery_locations, cur_per=current_percentage, rem_time=remaining_time, loc_url=location_url)

##############
#   API      #
##############
@app.route('/location/api/delivery/robot_location', methods=['GET', 'POST'])
def get_robot_location():
    if request.method == "GET":
        return jsonify(delivery['Robot_Location'])
    elif request.method == "POST":
        delivery['Robot_Location'] = [float(request.form['lat']),float(request.form['long'])] 
        return jsonify({'Updated_Robot_Location': delivery['Robot_Location']}), 201
    else:
        abort(404)


@app.route('/location/api/delivery/delivery_location', methods=['GET', 'POST'])
def get_delivery_location():
    if request.method == "GET":
        return jsonify(delivery['Delivery_Location'])
    elif request.method == "POST":
        delivery['Delivery_Location'] = [float(request.form['lat']),float(request.form['long'])] 
        return jsonify({'Updated_Delivery_Location': delivery['Delivery_Location']}), 201

    else:
        abort(404)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
