create or replace view trips_bronze as
select 
	region,
	st_geogfromtext(origin_coord) as origin,
	st_geogfromtext(destination_coord) as destination,
	to_timestamp(datetime, 'YYYY-MM-DD HH24:MI:SS') as datetime,
	datasource
from trips_raw
;
