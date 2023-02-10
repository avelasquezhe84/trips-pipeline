from dask import dataframe as ddf
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

URI = "postgresql+psycopg2://postgres:password@localhost:5432/tripsdb"

def read_data(url: str) -> ddf:
    return ddf.read_csv(url)

def truncate_table(table: str) -> None:
    engine = create_engine(URI, pool_size=10, max_overflow=20)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.execute(text('''TRUNCATE TABLE {}'''.format(table)))
    session.commit()
    session.close()
    engine.dispose()

def create_views():
    engine = create_engine(URI, pool_size=10, max_overflow=20)
    with engine.connect() as connection:
        query = open("sql/trips_bronze.sql").read()
        connection.execute(text(query))
        query = open("sql/trips_silver.sql").read()
        connection.execute(text(query))

def load_data(df: ddf) -> None:
    table = "trips_raw"
    truncate_table(table)
    df.to_sql(table, URI, if_exists="append", index=False, chunksize=100_000, method="multi", parallel=True)
    create_views()

def get_weekly_average_by_bounding_box(min_lat: float, min_lon: float, max_lat: float, max_lon: float):
    query = open("sql/trips_gold_weekly_average_by_bounding_box.sql").read().format(min_lon=min_lon, min_lat=min_lat, max_lon=max_lon, max_lat=max_lat)
    engine = create_engine(URI, pool_size=10, max_overflow=20)
    with engine.connect() as connection:
        result = connection.execute(text(query))
        result = result.first()[0]
        result = round(float(result), 2)
        result = str(result)
    engine.dispose()
    return result

def get_weekly_average_by_region(region: str):
    query = open("sql/trips_gold_weekly_average_by_region.sql").read().format(region=region)
    engine = create_engine(URI, pool_size=10, max_overflow=20)
    with engine.connect() as connection:
        result = connection.execute(text(query))
        result = result.first()[0]
        result = round(float(result), 2)
        result = str(result)
    engine.dispose()
    return result

def main(source: str, url: str) -> None:
    if source == "GDrive":
        # url = "https://drive.google.com/file/d/14JcOSJAWqKOUNyadVZDPm7FplA7XYhrU/view"
        url = "https://drive.google.com/uc?id=" + url.split("/")[-2]
    df = read_data(url)
    load_data(df)
