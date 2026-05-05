CREATE DATABASE IF NOT EXISTS my_database;
USE my_database;

CREATE TABLE IF NOT EXISTS titanic (
    PassengerId INT PRIMARY KEY,
    Survived INT,
    Pclass INT,
    Name VARCHAR(255),
    Sex VARCHAR(10),
    Age FLOAT NULL,
    SibSp INT,
    Parch INT,
    Ticket VARCHAR(50),
    Fare FLOAT,
    Cabin VARCHAR(50) NULL,
    Embarked VARCHAR(10) NULL
);

LOAD DATA INFILE '/var/lib/mysql-files/titanic.csv'
INTO TABLE titanic
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(PassengerId, Survived, Pclass, Name, Sex, @vAge, SibSp, Parch, Ticket, Fare, @vCabin, @vEmbarked)
SET
    Age = NULLIF(@vAge, ''),
    Cabin = NULLIF(@vCabin, ''),
    Embarked = NULLIF(@vEmbarked, '');