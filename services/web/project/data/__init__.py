from dask import dataframe as ddf
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

class LoadData():

    def __init__(self, URI: str) -> None:
        self.URI = URI
        engine = create_engine(URI, pool_size=10, max_overflow=20)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        self.session.close()
        self.engine.dispose()

    def read_data(self, url: str) -> ddf:
        return ddf.read_csv(url)

    def truncate_table(self, table: str) -> None:
        self.session.execute(text("TRUNCATE TABLE {}".format(table)))
        self.session.commit()

    def create_bronze_table(self):
        filepath = os.path.join(os.getcwd(), "sql")
        query = open(os.path.join(filepath, "trips_bronze.sql")).read()
        self.session.execute(text(query))
        self.session.commit()

    def create_silver_table(self):
        filepath = os.path.join(os.getcwd(), "sql")
        query = open(os.path.join(filepath, "trips_silver.sql")).read()
        self.session.execute(text(query))
        self.session.commit()

    def load_data(self, df: ddf) -> None:
        table = "trips_raw"
        self.truncate_table(table)
        df.to_sql(table, self.URI, if_exists="append", index=False, chunksize=100_000, method="multi", parallel=True)
        self.create_bronze_table()
        self.create_silver_table()

    def get_weekly_average_by_bounding_box(self, min_lat: float, min_lon: float, max_lat: float, max_lon: float):
        filepath = os.path.join(os.getcwd(), "sql")
        query = open(os.path.join(filepath, "trips_gold_weekly_average_by_bounding_box.sql")).read().format(min_lon=min_lon, min_lat=min_lat, max_lon=max_lon, max_lat=max_lat)
        result = self.session.execute(text(query))
        result = result.first()[0]
        result = round(float(result), 2)
        result = str(result)
        return result

    def get_weekly_average_by_region(self, region: str):
        filepath = os.path.join(os.getcwd(), "sql")
        query = open(os.path.join(filepath, "trips_gold_weekly_average_by_region.sql")).read().format(region=region)
        result = self.session.execute(text(query))
        result = result.first()[0]
        result = round(float(result), 2)
        result = str(result)
        return result

    def main(self, source: str, url: str) -> None:
        if source == "GDrive":
            # url = "https://drive.google.com/file/d/14JcOSJAWqKOUNyadVZDPm7FplA7XYhrU/view"
            url = "https://drive.google.com/uc?id=" + url.split("/")[-2]
        df = self.read_data(url)
        self.load_data(df)
