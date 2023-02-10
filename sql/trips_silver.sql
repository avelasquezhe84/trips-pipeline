create or replace view trips_silver as
with cte as (
  select distinct on (region, origin, destination, trip_hour)
         region, 
         st_geomfromtext('point(' || round(st_x(origin::geometry)::numeric, 4) || ' ' || round(st_y(origin::geometry)::numeric, 4) || ')') as origin, 
         st_geomfromtext('point(' || round(st_x(destination::geometry)::numeric, 4) || ' ' || round(st_y(destination::geometry)::numeric, 4) || ')') as destination, 
         date_trunc('hour', datetime) as trip_hour, datetime
  from trips_bronze
  order by region, origin, destination, trip_hour, datetime desc
)
select region, origin, destination, trip_hour, count(*) as trip_count
from cte
group by region, origin, destination, trip_hour
;
