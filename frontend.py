from flask import Flask, render_template, url_for
app = Flask(__name__)

current_percentage = 0
remaining_time = 100

food_items = ["sandwhich","soda","candy"]
delivery_locations = ["Foley Library", "Hemmingson NW Corner", "Herak NE Corner"]

@app.route("/")
def hello():
    return render_template("home.html", title="GUADR Mockup" , foods=food_items, locations=delivery_locations, cur_per=current_percentage, rem_time=remaining_time)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

