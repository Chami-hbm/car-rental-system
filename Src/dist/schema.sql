-- Database schema
CREATE DATABASE IF NOT EXISTS car_rental;
USE car_rental;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(60),
    role ENUM('admin', 'customer'),
    rentals_count INT DEFAULT 0,
    last_rental_date DATE
);

CREATE TABLE cars (
    id INT PRIMARY KEY AUTO_INCREMENT,
    make VARCHAR(50),
    model VARCHAR(50),
    year INT,
    daily_price DECIMAL(10,2),
    min_rent INT,
    max_rent INT,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE rentals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    car_id INT,
    start_date DATE,
    end_date DATE,
    status ENUM('pending', 'approved', 'rejected'),
    total_price DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (car_id) REFERENCES cars(id)
);
