select 
    avg(count)
from (
    select
        date_trunc('week', datetime) AS trip_week, 
        count(*)
    from trips_silver
    where st_within(origin::geometry, st_makeenvelope({min_long}, {min_lat}, {max_long}, {max_lat}, 4326))
    or st_within(destination::geometry, st_makeenvelope({min_long}, {min_lat}, {max_long}, {max_lat}, 4326))
    group by trip_week
)
;
