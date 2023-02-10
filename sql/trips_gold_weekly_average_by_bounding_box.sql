select 
    avg(count)
from (
    select
        date_trunc('week', trip_hour) AS trip_week, 
        count(*)
    from trips_silver
    where st_within(origin::geometry, st_makeenvelope({min_lon}, {min_lat}, {max_lon}, {max_lat}))
    or st_within(destination::geometry, st_makeenvelope({min_lon}, {min_lat}, {max_lon}, {max_lat}))
    group by trip_week
) t
;
