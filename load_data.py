from dask import dataframe as ddf

def read_data(url: str) -> ddf:
    return ddf.read_csv(url)

def load_data(df: ddf, uri: str) -> None:
    df.to_sql("trips_raw", uri, if_exists="replace", index=False, chunksize=1000, method="multi", parallel=True)

def main() -> None:
    print("Running...")
    url = "https://drive.google.com/file/d/14JcOSJAWqKOUNyadVZDPm7FplA7XYhrU/view"
    url = "https://drive.google.com/uc?id=" + url.split("/")[-2]
    df = read_data(url)
    uri = "postgresql+psycopg2://postgres:password@localhost:5432/tripsdb"
    load_data(df, uri)

if __name__ == "__main__":
    main()
