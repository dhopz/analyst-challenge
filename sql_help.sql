INSERT INTO vehicle (vehicle_spec_id, year, make, model, drivetrain, max_torque, max_horsepower, max_horsepower_rpm, max_torque_rpm, engine_displacement, fuel_type, fuel_tank_capacity, fuel_economy_city, fuel_economy_highway, cylinders, forced_induction, device_generation)
VALUES (1000502,2016,'Hyundai','Creta',2,260,126,4000,1500,1.582,1059,55,19.67,24.1,4,NULL,3);

DROP TABLE drive CASCADE;

CREATE TABLE drive (
    id SERIAL PRIMARY KEY,
    trip_id VARCHAR (50),
    datetime TIMESTAMP NOT NULL,
    vehicle_spec_id INT,
    engine_coolant_temp DECIMAL,
    eng_load DECIMAL,
    fuel_level DECIMAL,
    iat DECIMAL,
    rpm DECIMAL,
    lat DECIMAL,
    long DECIMAL,
    velocity DECIMAL
    );

CREATE TABLE vehicle (
    vehicle_spec_id INT PRIMARY KEY,
    year INT,
    make VARCHAR (50),
    Model VARCHAR (50),
    drivetrain INT,
    max_torque INT,
    max_horsepower INT,
    max_horsepower_rpm INT,
    max_torque_rpm INT,
    engine_displacement DECIMAL,
    fuel_type INT,
    fuel_tank_capacity INT,
    fuel_economy_city DECIMAL,
    fuel_economy_highway DECIMAL,
    cylinders INT,
    forced_induction INT DEFAULT NULL,
    device_generation INT,
    UNIQUE (vehicle_spec_id)
    );

ALTER TABLE vehicle
    ADD CONSTRAINT vehicle_pk PRIMARY KEY (vehicle_spec_id);

SELECT 
drive.vehicle_spec_id, 
trip_id,
ROUND(AVG(eng_load/255)*100,2) AS average_eng_load_perc,
ROUND(AVG(velocity),2) AS average_velocity,
ROUND(MAX((drive.fuel_level / 255) * vehicle.fuel_tank_capacity),2) - ROUND(MIN((drive.fuel_level / 255) * vehicle.fuel_tank_capacity),2) AS fuel_used
FROM drive
INNER JOIN vehicle on vehicle.vehicle_spec_id = drive.vehicle_spec_id
GROUP BY trip_id, drive.vehicle_spec_id;

--Notes - fuel used doesn't quite look right, for example the below trip ID has a datetime column which is by the second, then fuel level goes up and down ,There could be a calibration issue
-- or elevation, I just used min and max to give an indication of the fuel used.

SELECT COUNT(id) FROM drive
WHERE trip_id = '00922df3be5a4589ab385d0c2da2dd81';

SELECT COUNT(id) FROM drive
INNER JOIN vehicle on vehicle.vehicle_spec_id = drive.vehicle_spec_id;

SELECT datetime, trip_id, make, model, lat, long, CONCAT(lat, ',',long) as coordinates
FROM drive
INNER JOIN vehicle on vehicle.vehicle_spec_id = drive.vehicle_spec_id
WHERE trip_id = '00922df3be5a4589ab385d0c2da2dd81';