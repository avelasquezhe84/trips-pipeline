create or replace view public.trips_bronze as
select 
	region,
	st_geogfromtext(origin_coord) as origin,
	st_clusterkmeans(st_geomfromtext(origin_coord), 100) over() as origin_cluster,
	st_clusterkmeans(st_geomfromtext(destination_coord), 100) over() as destination_cluster,
	to_timestamp(datetime, 'YYYY-MM-DD HH24:MI:SS') as datetime,
	datasource
from public.trips_raw
;
