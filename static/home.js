var default_latitude_offset = 0.000633;
var default_longitude_offset = 0.000755;
var herak_lat = 47.666859;
var herak_long = -117.401717;
var foley_lat = 47.666668;
var foley_long = -117.400645;
var hemm_lat = 47.667322;
var hemm_long = -117.399905;
var crosby_lat = 47.667456;
var crosby_long = -117.401291;
var default_layer = "mapnik";
var chosen_Location = "";
var user_lat = 0;
var user_long = 0;
var delivery_lat = 0;
var delivery_long = 0;
var delivery_dictionary = {}

//load every 5 seconds
var mapLoadInterval = setInterval(updateBotLocation, 5000); //5 seconds

//define variables to see if the position of the bot has moved
var lastLat = 47.666867;
var lastLong = -117.4017010;

function updateMap(){
	//if the bot has moved, reload the page
	if( (this.response[0]["latitude"] !== lastLat) || (this.response[0]["longitude"]!== lastLong) ){
		var url = generateUrl(this.response[0]["latitude"], this.response[0]["longitude"], default_latitude_offset, default_longitude_offset, default_layer);
		document.getElementById("openstreetmap").src=url;
		lastLat = this.response[0]["latitude"];
		lastLong = this.response[0]["longitude"];
	}
}

function updateBotLocation(){
	var xhr = new XMLHttpRequest(); //create xml request
	xhr.addEventListener("load", updateMap); //call function on load
	xhr.responseType = "json";
	xhr.open("GET", "/location/api/delivery/robot_location", true);
	xhr.send();
}


// takes in latitude, longitude, and offsets
// returns Open Street Maps GUI for
function generateUrl(lat, long, lat_offset, long_offset, layer){
	var url = "https://www.openstreetmap.org/export/embed.html?bbox=";
	var delimeter = "%2C";
	url = url + (long - long_offset) + delimeter + (lat - lat_offset) + delimeter;
	url = url + (long + long_offset) + delimeter + (lat + lat_offset);
	url = url + "&layer=" + layer + "&marker=" + lat + delimeter + long;
	return url;
}			

var layer_selector = document.getElementById("map-layer-selector");
layer_selector.addEventListener('change', function() {
	default_layer=this.value;
}, false);


window.addEventListener("load", function() {
	document.getElementById("order-button").addEventListener("click", function(){
		if(chosen_Location === ""){
			alert("You have not chosen a delivery location. If you have chosen a user specified location, please press 'load specified location'")	
		}
		else{
			delivery_dictionary.latitude = delivery_lat;
			delivery_dictionary.longitude = delivery_long;
			document.getElementById("delivery-status-container").style.display = "block";

			
			var xhr = new XMLHttpRequest();
			var data = new FormData();
			data.append("latitude",delivery_lat);
			data.append("longitude",delivery_long);
			xhr.open('POST', '/location/api/delivery/delivery_location');
			xhr.send(data);
		}
	});

	// event listener for "Load map" button
	document.getElementById("map-go-button").addEventListener("click", function(){
		user_lat = parseFloat(document.getElementById("lat-enter").value);
		user_long = parseFloat(document.getElementById("long-enter").value);
		var url = generateUrl(user_lat, user_long, default_latitude_offset, default_longitude_offset, default_layer);
		document.getElementById("openstreetmap").src=url;
		chosen_Location = "custom";
		delivery_lat = user_lat;
		delivery_long = user_long;
	});

	// event listener for "Herak" button
	document.getElementById("herak-go-button").addEventListener("click", function(){
		var url = generateUrl(herak_lat, herak_long, default_latitude_offset, default_longitude_offset, default_layer);
		document.getElementById("openstreetmap").src=url;
		chosen_Location = "herak";
		delivery_lat = herak_lat;
		delivery_long = herak_long;

	});

	// event listener for "Foley" button
	document.getElementById("foley-go-button").addEventListener("click", function(){
		var url = generateUrl(foley_lat, foley_long, default_latitude_offset, default_longitude_offset, default_layer);
		document.getElementById("openstreetmap").src=url;
		chosen_Location = "foley";
		delivery_lat = foley_lat;
		delivery_long = foley_long;

	});
	// event listener for "Hemmingson" button
	document.getElementById("hemm-go-button").addEventListener("click", function(){
		var url = generateUrl(hemm_lat, hemm_long, default_latitude_offset, default_longitude_offset, default_layer);
		document.getElementById("openstreetmap").src=url;
		chosen_Location = "hemmingson";
		delivery_lat = hemm_lat;
		delivery_long = hemm_long;
	});
	// event listener for "Crosby" button
	document.getElementById("crosby-go-button").addEventListener("click", function(){
		var url = generateUrl(crosby_lat, crosby_long, default_latitude_offset, default_longitude_offset, default_layer);
		document.getElementById("openstreetmap").src=url;
		chosen_Location = "crosby";
		delivery_lat = crosby_lat;
		delivery_long = crosby_long;

	});
});

