-- script that prepares a MySQL server for the project

-- to create the database:
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- to creat a new user with its password:
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- privileges to user:
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
