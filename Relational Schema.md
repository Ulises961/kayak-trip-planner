Relational Schema

Entities
User(<u>id</u>, mail, pwd, salt, phone, name)
Log(<u>id</u>, hours,avg_sea) inclusion : Log[id] ⊆ user_has_log[log]
Trip(<u>inventory</u>, <u>itinerary</u>)fk:Trip[inventory] ⊆ Inventory[id], fk[itinerary]⊆ Itinerary[id] inclusion : Trip[inventory,itinerary] ⊆ user_has_trip[inventory,itinerary]
Inventory(<u>id</u>)
Item(<u>id</u>, category, checked, name)
Itinerary(<u>id</u>, is_public, total_miles, expected_total_miles)inclusion: Itinerary[id] ⊆ Day[itinerary]
Day(<u>day_number</u>,<u>date</u>, <u>itinerary</u>) fk: Day[itinerary] ⊆ Itinerary[id]
Sea(<u>day_number</u>,<u>itinerary</u>,<u>date</u>, moon_phase, hight_tide, low_tide)fk: Sea[day_number,date,ininerary] ⊆ Day[day_number,date,itinerary]
Sea_state(<u>sea_day_number</u>, <u>sea_itinerary</u>, <u>sea_date</u>,<u>time</u>,wave_height, wave_direction, swell_direction, swell_period)
Weather(<u>day_number</u>,<u>itinerary</u>,<u>date</u>, model), fk:Weather[day_number,date,itinerary] ⊆ Day[day_number,date,itinerary]
Weather_state(<u>day_number</u>, <u>itinerary</u>,<u>date</u>,<u>time</u>, temperature, cloud, precipitation, wind_direction, wind_force), fk: weather_state[day_number,itinerary,date]  ⊆ Sea[day_number,itinerary,date]
Point(<u>id</u>,gps, notes)
Point_type(<u>id</u>, name)
Image(<u>id</u>, size, name, location)

Relationships


user_has_trip(<u>user</u>, <u>inventory</u>, <u>itinerary</u>)fk:user_has_trip[inventory,itinerary] ⊆ Trip[inventory,itinerary]
inventory_has_item(<u>inventory</u>, <u>item</u>)fk:inventory_has_item[inventory] ⊆ Inventory[id], fk inventory_has_item[item]⊆ Item[id]
user_endorses_log(<u>log</u>, <u>endorser</u>, <u>endorsed</u>)fk user_endorses_log[log]⊆ Log[id], user_endorses_log[user]⊆ User[id]
user_has_log(<u>log</u>, user)fk user_has_log[log]⊆ Log[id], user_has_log[user] ⊆ User[id]
user_has_profile_picture(<u>user</u>, picture)fk user_has_picture[user]⊆ User[id], user_has_profile_picture[picture] ⊆ Image[id]
point_has_image(<u>image_id</u>, point_id)fk point_has_image[image_id]⊆ image[id], point_has_image[point_id] ⊆ Point[id]
point_is_nearby(reference_point_id, nearby_point_id) fk point_is_nearby[reference_point, nearby_point]⊆ Point[id] 
point_previous_next(prev_point_id,* next_point_id*, <u>curr_point_id</u>)fk point_previous_next[prev_point_id, next_point_id, curr_point_id] ⊆ Point[id]
point_has_type[<u>type</u>, point_id] fk point_has_type[type] ⊆ Type[id], point_has_type[point_id]⊆ Point[id]