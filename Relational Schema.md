Relational Schema

Entities
User(<u>id</u>, mail, pwd, salt, phone, name)
Log(<u>id</u>, hours,avg_sea) inclusion : Log[id] ⊆ user_has_log[log]
Trip(<u>inventory</u>, <u>itinerary</u>)fk:Trip[inventory] ⊆ Inventory[id], fk[itinerary]⊆ Itinerary[id]
Inventory(<u>id</u>)
Item(<u>id</u>, category, checked, name)
Itinerary(<u>id</u>, is_public, total_miles, expected_total_miles)inclusion: Itinerary[id] ⊆ Day[itinerary]
Day(<u>day_number</u>,<u>date</u>, <u>itinerary</u>) fk: Day[itinerary] ⊆ Itinerary[id]
Sea(<u>day_number</u>,<u>itinerary</u>,<u>date</u>, moon_phase, hight_tide, low_tide)fk: Sea[day_number] ⊆ Day[day_number],Sea[itinerary] ⊆ Day[itinerary],Sea[date] ⊆ Day[date]
Sea_state(<u>sea_day_number</u>, <u>sea_itinerary</u>,<u>time</u>,wave_height, wave_direction, swell_direction, swell_period)
Weather(<u>day_number</u>,<u>itinerary</u>,<u>date</u>, time), fk:Weather[day_number] ⊆ Day[day_number],Weather[itinerary] ⊆ Day[itinerary],Weather[date] ⊆ Day[date]
Weather_state(<u>day_number</u>, <u>itinerary</u>,<u>time</u>, temperature, cloud, precipitation, wind_direction, wind_force), fk: weather_state[day_number]  ⊆ Sea[day_number], weather_state[itinerary]  ⊆ Sea[itinerary], weather_state[date]  ⊆ Sea[date]
Point(<u>day_number</u>, <u>itinerary</u>,<u>gps</u>,<u>date</u> notes)fk:day_has_points[day_number]  ⊆ Day[day_number],day_has_points[itinerary]  ⊆ Day[itinerary], day_has_points[date]  ⊆ Day[date]
Point_type(<u>id</u>, name)
Image(<u>id</u>, size, name, location)

Relationships


user_has_trip(<u>user</u>, <u>inventory</u>, <u>itinerary</u>)fk:user_has_trip[inventory] ⊆ Trip[inventory], fk user_has_trip[itinerary]⊆ Trip[itinerary]
inventory_has_item(<u>inventory</u>, <u>item</u>)fk:inventory_has_item[inventory] ⊆ Inventory[id], fkinventory_has_item[item]⊆ Item[id]
user_endorses_log(<u>log</u>, user)fk user_endorses_log[log]⊆ Log[id], user_endorses_log[user]⊆ User[id]
user_has_log(<u>log</u>, user)fk user_has_log[log]⊆ Log[id], user_has_log[user] ⊆ User[id]
user_has_profile_picture(<u>user</u>, picture)fk user_has_picture[user]⊆ User[id], user_has_profile_picture[picture] ⊆ Picture[id]