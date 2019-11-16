DROP TABLE IF EXISTS delivery_location;
DROP TABLE IF EXISTS robot_location;

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
	FOREIGN KEY (del_id) REFERENCES delivery_location (delivery_id)
);

INSERT INTO delivery_location ( latitude, longitude) VALUES(
	47.666867,
	-117.4017010);

INSERT INTO robot_location (del_id, time, latitude, longitude ) VALUES(
	1,
	datetime('now','localtime'),
	47.666867,
	-117.4017010);

