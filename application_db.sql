CREATE TYPE point_type AS ENUM ('stop', 'position', 'interest');
CREATE TYPE item_category AS ENUM ('first_aid', 'camping', 'repair', 'travel', 'generic');


CREATE TABLE
    Users (
        id SERIAL PRIMARY KEY,
        mail VARCHAR(255) NOT NULL,
        pwd VARCHAR(255) NOT NULL,
        salt VARCHAR(255),
        phone NUMERIC UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255)
    );

CREATE TABLE
    Itinerary (
        id SERIAL PRIMARY KEY,
        is_public BOOLEAN,
        total_miles NUMERIC,
        expected_total_miles NUMERIC
    );

CREATE TABLE
    Inventory (id SERIAL PRIMARY KEY);

CREATE TABLE
    Log (
        id SERIAL PRIMARY KEY,
        hours NUMERIC,
        avg_sea NUMERIC
    );

CREATE TABLE
    Trip (
        inventory_id INTEGER,
        itinerary_id INTEGER,
        PRIMARY KEY (inventory_id, itinerary_id)
    );

CREATE TABLE
    Item (
        id SERIAL PRIMARY KEY,
        category item_category DEFAULT 'generic',
        checked BOOLEAN,
        name VARCHAR(255)
    );


CREATE TABLE
    Day (
        day_number INTEGER,
        date DATE,
        itinerary_id INTEGER,
        PRIMARY KEY (day_number, date, itinerary_id)
    );

CREATE TABLE
    day_has_points (
        day_number INTEGER NOT NULL,
        date DATE NOT NULL,
        itinerary_id INTEGER NOT NULL,
        point_id INTEGER NOT NULL,
        PRIMARY KEY (day_number, date, itinerary_id, point_id)
    );

CREATE TABLE
    Sea (
        day_number INTEGER,
        itinerary_id INTEGER,
        date DATE,
        moon_phase VARCHAR(255),
        high_tide TIME,
        low_tide TIME,
        PRIMARY KEY (day_number, date, itinerary_id)
    );

CREATE TABLE
    Sea_state (
        day_number INTEGER,
        itinerary_id INTEGER,
        date DATE,
        time TIME,
        wave_height NUMERIC,
        wave_direction NUMERIC,
        swell_direction NUMERIC,
        swell_period NUMERIC,
        PRIMARY KEY (day_number, date, itinerary_id, time)
    );

CREATE TABLE
    Weather (
        day_number INTEGER,
        itinerary_id INTEGER,
        date DATE,
        time TIME,
        model VARCHAR(255),
        PRIMARY KEY (day_number, date, itinerary_id)
    );

CREATE TABLE
    Weather_state (
        day_number INTEGER,
        date DATE,
        itinerary_id INTEGER,
        time TIME,
        temperature NUMERIC,
        cloud VARCHAR(255),
        precipitation NUMERIC,
        wind_direction NUMERIC,
        wind_force NUMERIC,
        PRIMARY KEY (day_number, date, itinerary_id, time)
    );

CREATE TABLE
    Point (
        id SERIAL PRIMARY KEY,
        gps NUMERIC,
        notes TEXT,
        type point_type DEFAULT 'position'
    );


CREATE TABLE
    Image (
        id SERIAL PRIMARY KEY,
        size NUMERIC,
        name VARCHAR(255),
        location VARCHAR(255)
    );

CREATE TABLE
    User_has_trip (
        user_id INTEGER,
        inventory_id INTEGER,
        itinerary_id INTEGER,
        PRIMARY KEY (user_id, inventory_id, itinerary_id)
    );

CREATE TABLE
    Inventory_has_item (
        inventory_id INTEGER,
        item_id INTEGER,
        PRIMARY KEY (inventory_id, item_id)
    );

CREATE TABLE
    User_endorses_log (
        log_id INTEGER,
        endorser INTEGER,
        endorsed INTEGER,
        PRIMARY KEY (log_id, endorser, endorsed)
    );

CREATE TABLE
    User_has_log (
        log_id INTEGER PRIMARY KEY, 
        user_id INTEGER
    );

CREATE TABLE
    User_has_profile_picture (
        user_id INTEGER PRIMARY KEY,
        image_id INTEGER
    );

CREATE TABLE
    Point_has_image (
        image_id INTEGER PRIMARY KEY, 
        point_id INTEGER
    );

CREATE TABLE
    Point_previous_next (
        current_point_id INTEGER PRIMARY KEY,
        previous_point_id INTEGER NULL,  
        next_point_id INTEGER NULL
    );

CREATE TABLE
    Point_is_nearby (
        reference_point_id INTEGER,
        nearby_point_id INTEGER, 
        PRIMARY KEY(reference_point_id,nearby_point_id)
    );

CREATE TABLE 
    Point_has_type (
        point_id INTEGER,
        type_id INTEGER,
        PRIMARY KEY (point_id, type_id)
    );

ALTER TABLE
    Point_has_image ADD CONSTRAINT point_fkeys_in__point_has_image FOREIGN KEY (point_id) REFERENCES point (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT image_fkeys_in__point_has_image FOREIGN KEY (image_id) REFERENCES image (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE
    User_has_profile_picture ADD CONSTRAINT user_fkeys_in__User_has_profile_picture FOREIGN KEY (user_id) REFERENCES Users(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT image_fkeys_in__User_has_profile_picture FOREIGN KEY (image_id) REFERENCES image (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE
    User_has_log ADD CONSTRAINT log_fkeys_in__user_has_log FOREIGN KEY (log_id) REFERENCES Log (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT users_fkeys_in__user_has_log FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE
    User_endorses_log ADD CONSTRAINT log_fkeys_in__user_endorses_log FOREIGN KEY (log_id) REFERENCES Log (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT user_fkeys_in__user_endorses_log_as_endorsed FOREIGN KEY (endorsed) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT user_fkeys_in__user_endorses_log_as_endorser FOREIGN KEY (endorser) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE
    Inventory_has_item ADD CONSTRAINT inventory_fkeys_in__inventory_has_item FOREIGN KEY (inventory_id) REFERENCES Inventory (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT item_fkeys_in__inventory_has_item FOREIGN KEY (item_id) REFERENCES Item (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE
    User_has_trip ADD CONSTRAINT trip_fkeys_in__user_has_trip FOREIGN KEY (inventory_id, itinerary_id) REFERENCES Trip (inventory_id, itinerary_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT user_fkeys_in__user_has_trip FOREIGN KEY (user_id) REFERENCES Users (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE
    Day_has_points ADD CONSTRAINT day_fkeys_in__day_has_points FOREIGN KEY (date, day_number, itinerary_id) REFERENCES Day (date, day_number, itinerary_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT point_fkeys_in__day_has_points FOREIGN KEY (point_id) REFERENCES Point (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE
    Weather_state ADD CONSTRAINT weather_fkeys_in__weather_state FOREIGN KEY (date, day_number, itinerary_id) REFERENCES Weather (date, day_number, itinerary_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE
    Weather ADD CONSTRAINT day_fkeys_in__weather FOREIGN KEY (date, day_number, itinerary_id) REFERENCES Day (date, day_number, itinerary_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE
    Sea ADD CONSTRAINT day_fkeys_in__sea FOREIGN KEY (date, day_number, itinerary_id) REFERENCES Day (date, day_number, itinerary_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE
    Day ADD CONSTRAINT itinerary_fkeys_in__day FOREIGN KEY (itinerary_id) REFERENCES Itinerary (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE
    Trip ADD CONSTRAINT itinerary_fkeys_in__trip FOREIGN KEY (itinerary_id) REFERENCES Itinerary (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE
    Trip ADD CONSTRAINT inventory_fkeys_in__trip FOREIGN KEY (inventory_id) REFERENCES Inventory (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE Point_previous_next
    ADD CONSTRAINT point_fkeys_in__trip_as_current_point FOREIGN KEY (current_point_id) REFERENCES Point (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT point_fkeys_in__trip_as_previous_point FOREIGN KEY (previous_point_id) REFERENCES Point (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT point_fkeys_in__trip_as_next_point FOREIGN KEY (next_point_id) REFERENCES Point (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE Point_is_nearby
    ADD CONSTRAINT point_fkeys_in__point_is_nearby_as_reference_point FOREIGN KEY (reference_point_id) REFERENCES Point (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT point_fkeys_in__point_is_nearby_as_nearby_point FOREIGN KEY (nearby_point_id) REFERENCES Point (id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;


CREATE OR REPLACE FUNCTION includeItineraryInDay() RETURNS TRIGGER AS $include_function$
   BEGIN
      INSERT INTO Day(itinerary_id, date, day_number) VALUES (new.ID, CURRENT_DATE, 1);
      RETURN NEW;
   END;
$include_function$ LANGUAGE plpgsql;



