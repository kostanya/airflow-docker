DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS currency;

CREATE TABLE country (
    country_abbreviation VARCHAR(5),
    country_name VARCHAR(100),
    PRIMARY KEY (country_abbreviation)
);

CREATE TABLE currency (
    country_abbreviation VARCHAR(5),
    currency VARCHAR(5),
    PRIMARY KEY (country_abbreviation)
);