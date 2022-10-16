Relational Schema

Entities
User(<u>id</u>, mail, pwd, salt, phone, name)
Log(<u>id</u>, hours,avg_sea)
Trip(<u>inventory</u>, <u>itinerary</u>)fk:Trip[inventory] ⊆ Inventory[id], fk[itinerary]⊆ Itinerary[id]
Inventory(<u>id</u>)
Item(<u>id</u>, category, checked, name)
Itinerary(<u>id</u>, is_public, total_miles, expected_total_miles)inclusion: Itinerary[id] ⊆ Day[itinerary]
Day(<u>day_number</u>, date, <u>itinerary</u>) fk: Day[itinerary] ⊆ Itinerary[id]
Sea(<u>day_number</u>,<u>itinerary</u>, moon_phase, hight_tide, low_tide)fk: Sea[day_number] ⊆ Day[day_number],Sea[itinerary] ⊆ Day[itinerary],
Sea_state(<u>sea_day_number</u>, <u>sea_itinerary</u>,<u>time</u>,wave_height, wave_direction, swell_direction, swell_period)
Weather(<u>day_number</u>,<u>itinerary</u>, time), Weather[day_number] ⊆ Day[day_number],Sea[itinerary] ⊆ Day[itinerary]
Weather_state(<u>weather_day_number</u>, <u>weather_itinerary</u>,<u>time</u>, temperature, cloud, precipitation, wind_direction, wind_force)
Point(<u>weather_day_number</u>, <u>weather_itinerary</u>,<u>gps</u>, notes)
Point_type(<u>id</u>, name)
Image(<u>id</u>, size, name, location)

Relationships


user_has_trip(<u>user</u>, <u>inventory</u>, <u>itinerary</u>)fk:user_has_trip[inventory] ⊆ Trip[inventory], fk user_has_trip[itinerary]⊆ Trip[itinerary]
inventory_has_item(<u>inventory</u>, <u>item</u>)fk:inventory_has_item[inventory] ⊆ Inventory[id], fkinventory_has_item[item]⊆ Item[id]
