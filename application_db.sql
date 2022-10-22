CREATE TABLE
    User (
        id SERIAL PRIMARY KEY,
        mail VARCHAR(255),
        pwd VARCHAR(255),
        salt VARCHAR(255),
        phone NUMERIC UNIQUE,
        name VARCHAR(255),
        surname VARCHAR(255)
    );

CREATE TABLE
    Log (
        id SERIAL PRIMARY KEY,
        hours NUMERIC,
        avg_sea NUMERIC
    );

CREATE TABLE
    Trip (
        inventory SERIAL,
        itinerary SERIAL,
        PRIMARY KEY (inventory, itinerary)
    );

CREATE TABLE
    Inventory (id SERIAL PRIMARY KEY);

CREATE TABLE
    Item (
        id SERIAL PRIMARY KEY,
        category VARCHAR(255),
        checked BOOLEAN,
        name VARCHAR(255)
    );

CREATE TABLE
    Itinerary (
        id SERIAL PRIMARY KEY,
        is_public BOOLEAN,
        total_miles NUMERIC,
        expected_total_miles NUMERIC
    );

CREATE TABLE
    Day (
        day_number INTEGER,
        date DATE,
        itinerary INTEGER,
        PRIMARY KEY (day_number, date, itinerary)
    );

CREATE TABLE
    Sea (
        day_number INTEGER,
        itinerary INTEGER,
        date DATE,
        moon_phase VARCHAR(255),
        high_tide TIME,
        low_tide TIME,
        PRIMARY KEY (day_number, date, itinerary)
    );

CREATE TABLE
    Sea_state (
        day_number INTEGER,
        itinerary INTEGER,
        date DATE,
        time TIME,
        wave_height NUMERIC,
        wave_direction NUMERIC,
        swell_direction NUMERIC,
        swell_period NUMERIC,
        PRIMARY KEY (day_number, date, itinerary, time)
    );

CREATE TABLE
    Weather (
        day_number INTEGER,
        itinerary INTEGER,
        date DATE,
        time TIME,
        model VARCHAR(255),
        PRIMARY KEY (day_number, date, ininerary)
    );

CREATE TABLE
    Weather_state (
        day_number INTEGER,
        date DATE,
        itinerary INTEGER,
        time TIME,
        temperature NUMERIC,
        cloud VARCHAR(255),
        precipitation NUMERIC,
        wind_direction NUMERIC,
        wind_force NUMERIC,
        PRIMARY KEY (day_number, date, itinerary, time)
    );

CREATE TABLE
    Point (
        day_number INTEGER,
        itinerary INTEGER,
        gps NUMERIC,
        date DATE,
        notes TEXT,
        PRIMARY KEY (day_number, date, itinerary, gps)
    );

CREATE TABLE
    Point_type (id SERIAL PRIMARY KEY, name VARCHAR(255));

CREATE TABLE
    Image (
        id SERIAL PRIMARY KEY,
        size NUMERIC,
        name VARCHAR(255),
        location VARCHAR(255)
    );

CREATE TABLE
    user_has_trip (
        user,
        inventory,
        itinerary,
        PRIMARY KEY (user, inventory, itinerary)
    );

CREATE TABLE
    inventory_has_item (inventory, item, PRIMARY KEY (inventory, item));

CREATE TABLE
    user_endorses_log (
        log INTEGER,
        endorser INTEGER,
        endorsed INTEGER,
        PRIMARY KEY (log, endorser, endorsed)
    );

CREATE TABLE
    user_has_log (log INTEGER PRIMARY KEY, user INTEGER);

CREATE TABLE
    user_has_profile_picture (user INTEGER PRIMARY KEY, picture INTEGER);

CREATE TABLE
    point_has_image (
        image_id INTEGER PRIMARY KEY,
        itinerary INTEGER,
        date DATE,
        day_number INTEGER,
        gps NUMERIC
    );
    -- fk point_has_image[image_id]⊆ image[id], point_has_image[date,day_number,gps,itinerary] ⊆ Point[date,day_number,gps,itinerary]
    -- fk user_has_picture[user]⊆ User[id], user_has_profile_picture[picture] ⊆ Image[id]
    -- fk user_has_log[log]⊆ Log[id], user_has_log[user] ⊆ User[id]
    -- user_endorses_log[endorser] ⊆ User[id], user_endorses_log[endorsed]⊆ User[id]
    -- fk user_endorses_log[log]⊆ Log[id]
    -- fk:inventory_has_item[inventory] ⊆ Inventory[id];
    -- fk:user_has_trip[inventory,itinerary] ⊆ Trip[inventory,itinerary]
    -- fk inventory_has_item[item]⊆ Item[id]
    -- fk:day_has_points[day_number,date,itinerary]  ⊆ Day[day_number,date,itinerary]
    -- fk: weather_state[day_number,itinerary,date]  ⊆ Sea[day_number,itinerary,date]
    -- fk:Weather[day_number,date,itinerary] ⊆ Day[day_number,date,itinerary]
    -- fk: Sea[day_number,date,ininerary] ⊆ Day[day_number,date,itinerary]
    -- fk: Day[itinerary] ⊆ Itinerary[id]
    -- inclusion: Itinerary[id] ⊆ Day[itinerary]
    -- inclusion : Log[id] ⊆ user_has_log[log]
    -- fk:Trip[inventory] ⊆ Inventory[id], fk[itinerary]⊆ Itinerary[id] inclusion : Trip[inventory,itinerary] ⊆ user_has_trip[inventory,itinerary]
    -- inclusion: Itinerary[id] ⊆ Day[itinerary]