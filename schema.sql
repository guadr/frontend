DROP TABLE IF EXISTS delivery_location;
DROP TABLE IF EXISTS robot_location;
DROP TABLE IF EXISTS users;

CREATE TABLE delivery_location(
	delivery_id integer PRIMARY KEY AUTOINCREMENT,
	latitude DOUBLE not null,
	longitude DOUBLE not null,
	del_loc text,
	food_items text
);

CREATE TABLE robot_location(
	del_id integer not null,
	time TIMESTAMP not null DEFAULT CURRENT_TIMESTAMP,
	latitude DOUBLE not null,
	longitude DOUBLE not null,
	perc_complete DOUBLE not null,
	FOREIGN KEY (del_id) REFERENCES delivery_location (delivery_id)
);

CREATE TABLE users(
	username text not null,
	password text not null,
	vender integer default 0,
	id integer PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE vender(
	id integer,
	food_item text not null,
	food_price real not null

);

INSERT INTO delivery_location (delivery_id, latitude, longitude) VALUES(
	0,
	47.666867,
	-117.4017010);

INSERT INTO robot_location (del_id, time, latitude, longitude, perc_complete ) VALUES(
	0,
	datetime('now','localtime'),
	47.666867,
	-117.4017010,
	0.0);


