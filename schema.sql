DROP TABLE IF EXISTS delivery_location;
DROP TABLE IF EXISTS robot_location;
DROP TABLE IF EXISTS users;

CREATE TABLE delivery_location(
	delivery_id integer PRIMARY KEY AUTOINCREMENT,
	latitude DOUBLE not null,
	longitude DOUBLE not null
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
	id integer PRIMARY KEY AUTOINCREMENT
);

INSERT INTO delivery_location ( latitude, longitude) VALUES(
	47.666867,
	-117.4017010);

INSERT INTO robot_location (del_id, time, latitude, longitude, perc_complete ) VALUES(
	1,
	datetime('now','localtime'),
	47.666867,
	-117.4017010,
	0.0);


