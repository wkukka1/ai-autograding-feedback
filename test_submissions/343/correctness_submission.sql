-- Frequent traveler analysis (anonymized)

SET SEARCH_PATH TO SampleSchema;
DROP TABLE IF EXISTS result_q5 CASCADE;

CREATE TABLE result_q5 (
    user_id INT NOT NULL,
    contact_email VARCHAR(500) NOT NULL
);

-- Drop views if they exist
DROP VIEW IF EXISTS ViewA CASCADE;
DROP VIEW IF EXISTS ViewB CASCADE;
DROP VIEW IF EXISTS ViewC CASCADE;
DROP VIEW IF EXISTS ViewD CASCADE;

-- Sample view: join between flights and destination countries
CREATE VIEW ViewA AS
SELECT fid, country
FROM Flight
NATURAL JOIN Arrival
JOIN Route ON route = flight_num
JOIN Airport ON destination = code
JOIN City ON city = cid;

-- Users who visited at least 5 countries
CREATE VIEW ViewB AS
SELECT passenger AS user_id
FROM Booking
JOIN ViewA ON flight = fid
GROUP BY passenger
HAVING count(DISTINCT country) >= 5;

-- Users who booked at least 10 flights in 2023
CREATE VIEW ViewC AS
SELECT passenger AS user_id
FROM Booking
WHERE EXTRACT(YEAR FROM date_time) = 2023
GROUP BY passenger
HAVING count(DISTINCT flight) >= 10;

-- Users who booked more flights in 2024 than in 2023
CREATE VIEW ViewD AS
SELECT p.pid AS user_id
FROM Passenger p
WHERE (
    SELECT count(DISTINCT flight)
    FROM Booking
    WHERE p.pid = pid AND EXTRACT(YEAR FROM date_time) = 2024
) > (
    SELECT count(DISTINCT flight)
    FROM Booking
    WHERE p.pid = pid AND EXTRACT(YEAR FROM date_time) = 2023
);

-- Final query — still too strict (preserves the empty output error)
INSERT INTO result_q5
SELECT DISTINCT user_id, contact_email
FROM Passenger
NATURAL JOIN ViewB
NATURAL JOIN ViewC
NATURAL JOIN ViewD;
