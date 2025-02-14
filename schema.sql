DROP DATABASE IF EXISTS trash_pandas;
CREATE DATABASE trash_pandas;
\c trash_pandas;

-- Create tables

CREATE TABLE rank (
    rank_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    rank_name VARCHAR(50) NOT NULL UNIQUE,
    rank_seniority SMALLINT NOT NULL UNIQUE,
    CHECK (rank_seniority BETWEEN 1 AND 10),
    PRIMARY KEY (rank_id)
);

CREATE TABLE clan (
    clan_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    clan_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (clan_id)
);

CREATE TABLE item (
    item_id INT GENERATED ALWAYS AS IDENTITY,
    item_name VARCHAR(50) NOT NULL UNIQUE,
    edibility SMALLINT NOT NULL,
    CHECK (edibility BETWEEN 0 AND 10),
    PRIMARY KEY (item_id)
);

CREATE TABLE city (
    city_id INT GENERATED ALWAYS AS IDENTITY,
    city_name VARCHAR(50) NOT NULL,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL (10, 6) NOT NULL,
    PRIMARY KEY (city_id)
);

CREATE TABLE bin_type (
    type_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    type_name VARCHAR(25) NOT NULL UNIQUE,
    PRIMARY KEY (type_id)
);

CREATE TABLE bin (
    bin_id INT GENERATED ALWAYS AS IDENTITY,
    city_id INT NOT NULL,
    type_id SMALLINT NOT NULL,
    capacity SMALLINT NOT NULL,
    ease_of_access SMALLINT NOT NULL,
    PRIMARY KEY (bin_id),
    FOREIGN KEY (city_id) REFERENCES city(city_id),
    FOREIGN KEY (type_id) REFERENCES bin_type(type_id)
);

CREATE TABLE raccoon (
    raccoon_id INT GENERATED ALWAYS AS IDENTITY,
    raccoon_name VARCHAR(100) NOT NULL,
    date_of_birth TIMESTAMPTZ NOT NULL,
    gender VARCHAR(10),
    weight SMALLINT NOT NULL,
    colouring TEXT,
    rummaging_skill SMALLINT NOT NULL,
    PRIMARY KEY (raccoon_id),
    CHECK (date_of_birth < NOW()),
    CHECK (rummaging_skill BETWEEN 1 AND 10),
    CHECK (gender IN ('male', 'female', 'other', 'unknown'))
);

CREATE TABLE item_rummage (
    rummage_id INT GENERATED ALWAYS AS IDENTITY,
    item_id INT NOT NULL,
    raccoon_id INT NOT NULL,
    bin_id INT NOT NULL,
    rummaged_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (rummage_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id),
    FOREIGN KEY (raccoon_id) REFERENCES raccoon(raccoon_id),
    FOREIGN KEY (bin_id) REFERENCES bin(bin_id),
    CHECK (rummaged_at < NOW())
);

CREATE TABLE assign_raccoon_clan(
    assignment_id INT GENERATED ALWAYS AS IDENTITY,
    raccoon_id INT NOT NULL,
    clan_id SMALLINT NOT NULL,
    rank_id SMALLINT NOT NULL,
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (raccoon_id) REFERENCES raccoon(raccoon_id),
    FOREIGN KEY (clan_id) REFERENCES clan(clan_id),
    FOREIGN KEY (rank_id) REFERENCES rank(rank_id),
    UNIQUE (raccoon_id, clan_id)
);


-- Seed initial data

INSERT INTO rank (rank_name, rank_seniority)
VALUES 
    ('Raccoon Trainee', 1),
    ('Raccoon Apprentice', 2),
    ('Raccoon Scavenger', 3),
    ('Raccoon Forager', 4),
    ('Raccoon Skirmisher', 5),
    ('Raccoon Warrior', 6),
    ('Raccoon Manager', 7),
    ('Raccoon Deputy', 8),
    ('Raccoon Chief', 9),
    ('Raccoon Overlord', 10);


INSERT INTO clan (clan_name)
VALUES
    ('The Night Prowlers'),
    ('The Trash Pandas'),
    ('The Scheming Stalkers'),
    ('The Rampaging Rummagers'),
    ('The Foraging Friends');

INSERT INTO item (item_name, edibility)
VALUES 
    ('Syringe', 0),
    ('Chicken Bone', 5),
    ('Paper', 1),
    ('Leaves', 2),
    ('Feathers', 2),
    ('Steak', 10),
    ('Cake', 10),
    ('Plaster', 0),
    ('Human Remains', 7),
    ('Apple', 10),
    ('Banana Peel', 4),
    ('Rotting Fish', 3),
    ('Pizza Slice', 9),
    ('Onion', 2),
    ('Beer Can', 0),
    ('Mouldy Bread', 3),
    ('French Fries', 9),
    ('Cigarette Butt', 0),
    ('Chocolate Bar', 10),
    ('Carrot', 6),
    ('Rubber Glove', 0);

INSERT INTO bin_type (type_name)
VALUES
    ('General Waste'),
    ('Recycling'),
    ('Medical Waste');

INSERT INTO city (city_name, latitude, longitude)
VALUES 
    ('Binborough', 34.0522, -118.2437),
    ('Trashford', 40.7128, -74.0060),
    ('Pawston', 42.3601, -71.0589),
    ('Composton', 33.4484, -112.0740),
    ('Clawton', 35.2271, -80.8431);


INSERT INTO raccoon (raccoon_name, date_of_birth, 
    gender, weight, colouring, rummaging_skill)
VALUES
    ('Piggety Snicket', '2017-03-12', 'female', 25, 'grey with black paws', 7),
    ('Sister Gertrude', '2015-08-25', 'female', 28, 'black mask and white-tipped tail', 9),
    ('Charles', '2018-06-14', 'male', 22, 'silver and grey mix', 6),
    ('Max', '2016-09-30', 'other', 30, 'dark brown with grey ears', 7),
    ('T.J. Kreen', '2019-05-01', 'male', 24, 'classic black-and-white raccoon', 5),
    ('Goopu Loopu', '2020-11-18', 'unknown', 21, 'black spots on tail', 4),
    ('Mr. Denmark', '2014-02-20', 'male', 26, 'light grey fur with dark paws', 7),
    ('Glubtuppus Wepple', '2017-07-04', 'male', 29, 'dark mask and grey coat', 10),
    ('Gub Gub', '2016-12-12', 'male', 32, 'patchy fur with black streaks', 3),
    ('Eren', '2019-09-10', 'female', 23, 'brown and grey mix', 6),
    ('Giblet', '1998-01-01', 'other', 33, 'classic black-and-white-raccoon', 9),
    ('Francois Dubois', '2000-01-01', 'male', 22, 'beown and grey mix', 2),
    ('Bartholomew Trashford', '2018-03-21', 'male', 27, 'dark coat with white underbelly', 8),
    ('Chickenfingers', '2015-11-15', 'female', 28, 'silver and black striped coat', 9),
    ('Professor Crumb', '2014-05-27', 'male', 31, 'dark mask with grey-white fur', 1),
    ('Trashcan Terry (TT)', '2016-10-19', 'male', 30, 'light brown coat with black paws', 10),
    ('Pudding', '2018-10-10', 'female', 24, 'soft grey coat with brown highlights', 7),
    ('Jimothy Casserole', '2010-02-02', 'male', 70, 'classic black-and-white raccoon', 3),
    ('Lady Marmalade', '2019-06-23', 'female', 22, 'white-tipped ears with black fur', 5),
    ('Codsworth', '2024-01-09', 'female', 40, 'grey with white stripes', 8);