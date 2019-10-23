from flask import Flask, render_template, url_for
app = Flask(__name__)

current_percentage = 30
remaining_time = 100
latitude_robot = 47.667191
longitude_robot = -117.402382
latitude_destination = 47.666532
longitude_destination = -117.400659
lat_offset = 0.0063
long_offset = 0.00755
hc_location_url = "https://www.openstreetmap.org/export/embed.html?bbox=-117.4111032485962%2C47.66108082037928%2C-117.39591121673585%2C47.67368149482369&amp;layer=mapnik&amp;marker=47.66738153785244%2C-117.40350723266602"
location_url = "https://www.openstreetmap.org/export/embed.html?bbox=" + (str(longitude_destination - 0.00755)) + "%2C" + (str(latitude_destination - 0.0063)) + "%2C" + (str(longitude_destination + 0.00755)) + "%2C" + (str(latitude_destination - 0.0063)) + "&amp;layer=mapnik&amp;marker=" + (str(latitude_destination)) + "%2C" + (str(longitude_destination))

food_items = ["Sandwich","Soda","Candy","Trail Mix","Beef Jerky","Muffin"]
delivery_locations = ["Foley Library", "Hemmingson NW Corner", "Herak NE Corner", "Crosby North Entrance"]
latitudes_list = [latitude_robot, latitude_destination]
longitudes_list = [longitude_robot, longitude_destination]



@app.route("/")
def hello():
    return render_template("home.html", title="GUADR Mockup" , foods=food_items, locations=delivery_locations, cur_per=current_percentage, rem_time=remaining_time, loc_url=hc_location_url)

'''def convertLatituteLongitudeToUrl(latitude, longitude){
    return "https://www.openstreetmap.org/export/embed.html?bbox="
        + (longitude - 0.00755) + "%2C" + (latitude - 0.0063) + "%2C"
        + (longitude + 0.00755) + "%2C" + (latitude - 0.0063) + "&amp;layer=mapnik&amp;marker="
        + latitude + "%2C" + longitude
}'''

if __name__ == "__main__":
    app.run(host='0.0.0.0')
'''location_url = convertLatituteLongitudeToUrl(latitude_destination, longitude_destination)'''
