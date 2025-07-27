CREATE DATABASE IF NOT EXISTS ryanair_db;

DROP TABLE IF EXISTS airports;
CREATE TABLE airports (
    airport_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50),
    iata_code VARCHAR(10)
);

DROP TABLE IF EXISTS aircraft;
CREATE TABLE aircraft (
    aircraft_id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(50),
    capacity INT,
    range_km INT
);

DROP TABLE IF EXISTS flights;

CREATE TABLE flights (
    flight_id INT PRIMARY KEY,
    origin VARCHAR(10),
    destination VARCHAR(10),
    departure_time DATETIME,
    arrival_time DATETIME,
    aircraft_id INT,
    status VARCHAR(20),
    FOREIGN KEY (aircraft_id) REFERENCES aircraft(aircraft_id)
);

USE ryanair_db;
SHOW TABLES;

SELECT * FROM aircraft;
SELECT * FROM airports;
SELECT * FROM flights;

-- what aircraft is late the most 


SELECT 
    aircraft.model, 
    SUM(CASE WHEN status = 'delayed' THEN 1 ELSE 0 END) AS DL
FROM flights
LEFT JOIN aircraft ON aircraft.aircraft_id = flights.aircraft_id
GROUP BY aircraft.model
order by DL desc
limit 3;


SELECT 
    CASE WHEN destination = 'DUB' THEN 'DUB' ELSE 'Other' END AS destination_group,
    COUNT(*) AS total_flights
FROM flights
LEFT JOIN aircraft ON flights.aircraft_id = aircraft.aircraft_id
GROUP BY destination_group;

-- Top destinations 
SELECT 
	destination,
    count(*) AS total_flights
FROM flights
GROUP BY flight_id
ORDER BY total_flights DESC
LIMIT 3;

-- average delay by destiantion
select * from flights;
select * from flights;

SELECT 
	flight_id,
    status,
	AVG(timestampdiff(minute, departure_time, arrival_time)) AS avg_duration_minutes
FROM flights
WHERE status != "cancelled"
GROUP BY flight_id;


-- what origins have the most delayed flights 
SELECT 
    origin, 
    AVG(TIMESTAMPDIFF(MINUTE, departure_time, arrival_time)) AS avg_delayed_time
FROM flights
WHERE status = 'delayed'
GROUP BY origin
ORDER BY avg_delayed_time desc;

-- get all delayed flights
SELECT 
    flight_id, 
    aircraft_id,
    TIMESTAMPDIFF(MINUTE, departure_time, arrival_time) AS duration
FROM flights
ORDER BY duration DESC
LIMIT 1;

-- WHAT IS THE MOST RELIABLE AIRCRAFT?
select * from flights; 
select * from aircraft;

-- COUNT NUMBER OF FLIGHT BY DESTINATION 
SELECT 
	destination,
    COUNT(*) AS FLIGHTS_PER_DESTIANTION
FROM flights
GROUP BY destination 
ORDER BY  FLIGHTS_PER_DESTIANTION desc;

-- most reliable aricraft
SELECT 
	flights.aircraft_id, 
    aircraft.model, 
    COUNT(*) AS count_of_most_reliable,
    SUM(CASE WHEN status  = 'on time' THEN 1 ELSE 0 END) AS on_time_flights
from flights
LEFT JOIN aircraft 
	ON flights.aircraft_id = aircraft.aircraft_id
GROUP BY aircraft_id, model
HAVING COUNT(*) >= 5
ORDER BY count_of_most_reliable DESC;








