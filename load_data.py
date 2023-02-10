from dask import dataframe as ddf
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def read_data(url: str) -> ddf:
    return ddf.read_csv(url)

def truncate_table(table: str, uri: str) -> None:
    engine = create_engine(uri, pool_size=10, max_overflow=20)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.execute(text('''TRUNCATE TABLE {}'''.format(table)))
    session.commit()
    session.close()
    engine.dispose()

def load_data(df: ddf, uri: str) -> None:
    table = "trips_raw"
    truncate_table(table, uri)
    df.to_sql(table, uri, if_exists="append", index=False, chunksize=100_000, method="multi", parallel=True)

def main(source: str, url: str) -> None:
    if source == "GDrive":
        # url = "https://drive.google.com/file/d/14JcOSJAWqKOUNyadVZDPm7FplA7XYhrU/view"
        url = "https://drive.google.com/uc?id=" + url.split("/")[-2]
    df = read_data(url)
    uri = "postgresql+psycopg2://postgres:password@localhost:5432/tripsdb"
    load_data(df, uri)
