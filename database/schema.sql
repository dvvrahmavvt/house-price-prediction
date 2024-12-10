CREATE DATABASE housing_db;

USE housing_db;

CREATE TABLE prediction_result (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    bedroom_count INT,
    bathroom_count INT,
    carport_count INT,
    land_area DOUBLE,
    building_area DOUBLE,
    location_encoded INT,
    predicted_price DOUBLE
);
