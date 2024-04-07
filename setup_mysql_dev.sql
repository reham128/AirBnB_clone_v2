-- script that prepares a MySQL server for the project

-- to create the database:
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- to creat a new user with its password:
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- privileges to user:
GRANT ALL PRIVILEGES ON hbnb_dev_db . * TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema . * TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
