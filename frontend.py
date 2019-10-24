from flask import Flask, render_template, url_for
app = Flask(__name__)

current_percentage = 30
remaining_time = 100
latitude_robot = 47.667560
longitude_robot = -117.401629
latitude_destination = 47.666867
longitude_destination = -117.401701
lat_offset = 0.00633
long_offset = 0.00755
hc_location_url = "https://www.openstreetmap.org/?mlat=47.66753&mlon=-117.40291#map=18/47.66753/-117.40291"
location_url = "https://www.openstreetmap.org/export/embed.html?bbox=" + (str(longitude_destination - long_offset)) + "%2C" + (str(latitude_destination - lat_offset)) + "%2C" + (str(longitude_destination + long_offset)) + "%2C" + (str(latitude_destination + lat_offset)) + "&layer=mapnik&marker=" + (str(latitude_destination)) + "%2C" + (str(longitude_destination))

food_items = ["Sandwich","Soda","Candy","Trail Mix","Beef Jerky","Muffin"]
delivery_locations = ["Foley Library", "Hemmingson NW Corner", "Herak NE Corner", "Crosby North Entrance"]
latitudes_list = [latitude_robot, latitude_destination]
longitudes_list = [longitude_robot, longitude_destination]



@app.route("/")
def hello():
    return render_template("home.html", title="GUADR Mockup" , foods=food_items, locations=delivery_locations, cur_per=current_percentage, rem_time=remaining_time, loc_url=location_url)

'''def convertLatituteLongitudeToUrl(latitude, longitude){
    return "https://www.openstreetmap.org/export/embed.html?bbox="
        + (longitude - 0.00755) + "%2C" + (latitude - 0.0063) + "%2C"
        + (longitude + 0.00755) + "%2C" + (latitude - 0.0063) + "&amp;layer=mapnik&amp;marker="
        + latitude + "%2C" + longitude
}'''

if __name__ == "__main__":
    app.run(host='0.0.0.0')
'''location_url = convertLatituteLongitudeToUrl(latitude_destination, longitude_destination)'''
