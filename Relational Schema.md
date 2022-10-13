Relational Schema

Entities
User(<u>id</u>, mail, pwd, salt, phone, name)
Log(<u>id</u>, hours,avg_sea)
Trip(<u>id</u>)
Inventory(<u>id</u>)
Item(<u>id</u>, category, checked, name)
Itinerary(<u>id</u>, is_public, total_miles, expected_total_miles)
Day(<u>id</u>, day_number, date)
Sea(<u>id</u>, moon_phase, hight_tide, low_tide)
Sea_state(<u>id</u>, wave_height, wave_direction, swell_direction, swell_period)
Weather(<u>id</u>, time)
Weather_state(<u>id</u>, temperature, cloud, precipitation, wind_direction, wind_force)
Point(<u>id</u>, gps, notes)
Point_type(<u>id</u>, name)
Image(<u>id</u>, size, name, location)

Relationships
