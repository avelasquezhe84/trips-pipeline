select 
    avg(trip_count) as avg_trips
from (
    select 
        region,
        date_trunc('week', datetime) as trip_week,
        count(1) as trip_count
    from public.trips_bronze
    where region = {region}
    group by region, trip_week
) t
group by region
;