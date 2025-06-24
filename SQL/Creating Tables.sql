-- Creating all Tables in Tennis Database
-- 1. Categories Table
CREATE TABLE categories(
category_id VARCHAR(50) PRIMARY KEY,
category_name VARCHAR(100) NOT NULL
);

-- 2. Competitions Table
CREATE TABLE competitions(
competition_id VARCHAR(50) PRIMARY KEY,
competition_name VARCHAR(100) NOT NULL,
parent_id VARCHAR(50),
type VARCHAR(20) NOT NULL,
gender VARCHAR(10) NOT NULL,
category_id VARCHAR(50),
FOREIGN KEY (category_id) REFERENCES categories (category_id)
);

-- Replacing blank values with null values in parent id column
update competitions
set parent_id = NULL
where parent_id = '';

-- 3. Complexes Table
CREATE TABLE complexes(
complex_id VARCHAR(50) PRIMARY KEY,
complex_name VARCHAR(100) NOT NULL
);

-- 4. Venues Table
CREATE TABLE venues(
venue_id VARCHAR(50) PRIMARY KEY,
venue_name VARCHAR(100) NOT NULL,
city_name VARCHAR(100) NOT NULL,
country_name VARCHAR(100) NOT NULL,
country_code CHAR(3) NOT NULL,
timezone VARCHAR(100) NOT NULL,
complex_id VARCHAR(50),
FOREIGN KEY (complex_id) REFERENCES complexes (complex_id)
);

-- 5. Competitor Rankings Table
CREATE TABLE competitor_rankings (
rank_id INT PRIMARY KEY AUTO_INCREMENT,
`rank` INT NOT NULL,
movement INT NOT NULL,
points INT NOT NULL,
competitions_played INT NOT NULL,
competitor_id VARCHAR(50),
FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id)
);

-- 6. Competitors Table
CREATE TABLE competitors(
competitor_id VARCHAR(50) PRIMARY KEY,
name VARCHAR(100) NOT NULL,
country VARCHAR(100) NOT NULL,
country_code CHAR(3) NOT NULL,
abbreviation VARCHAR(10) NOT NULL
);
