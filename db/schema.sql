CREATE DATABASE IF NOT EXISTS monitoring_db;
USE monitoring_db;

CREATE TABLE IF NOT EXISTS system_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpu FLOAT,
    ram FLOAT,
    network BIGINT,
    disk FLOAT
);
