from datetime import datetime
import logging
import os
import time

import duckdb
import pandas as pd
import requests
from dotenv import load_dotenv

# Loading env credentials first to check if it works.
load_dotenv()
# Below we configure how the logging system behaves globally for this script.
logging.basicConfig(
# level=logging.INFO tells logger to show messages at INFO level and above (INFO, WARNING and ERROR)
    level=logging.INFO,
# format= defines what each log line will look like. Timestamp, level and message.
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# Creates a logger object to use across the script.
logger = logging.getLogger(__name__)

# Requesting access to the API via URL. Set the parameters as well.
BCB_BASE_URL = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados"
    "?formato=json&dataInicial={}&dataFinal={}"
)
SERIES = {
    "selic": 4390,
    "ipca": 16122,
}
START_DATE = "01/01/2014"
MOTHERDUCK_DB = "floripa_real_estate"
RAW_SCHEMA = "raw_bcb"

# Creates the function to access and fetch data from BCB API
def fetch_bcb_series(series_code: int, series_name: str) -> pd.DataFrame:
    """Fetches a time series from the BCB API.

    Args:
        series_code: The BCB series numeric identifier.
        series_name: Human readable name used for logging.

    Returns:
        A pandas DataFrame with columns 'data' and 'valor'.
    """

    end_date = datetime.today().strftime("%d/%m/%Y")
    url = BCB_BASE_URL.format(series_code, START_DATE, end_date)
    logger.info(f"Fetching {series_name} data from BCB API")

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            if attempt < 2:
                logger.warning(f"Attempt {attempt + 1} failed to request {series_name}. {e}")
                time.sleep(5)
            else:
                logger.error(f"All attempts failed for {series_name}. {e}")
                raise

    df = pd.DataFrame(response.json())
    return df

# Function to connect and load data into data warehouse.
# Args: DataFrame and series_name
def load_to_motherduck(df: pd.DataFrame, series_name: str) -> None:
    table_name = f"{MOTHERDUCK_DB}.{RAW_SCHEMA}.{series_name}"
    logger.info(f"Loading {series_name} data into MotherDuck")
    with duckdb.connect("md:") as con:
        con.execute(f"CREATE DATABASE IF NOT EXISTS {MOTHERDUCK_DB}")
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {MOTHERDUCK_DB}.{RAW_SCHEMA}")
        con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")

    logger.info(f"Successfully loaded {series_name} into {table_name}")

if __name__ == "__main__":
    logger.info("Starting BCB ingestion pipeline")

    for series_name, series_code in SERIES.items():
        df = fetch_bcb_series(series_code, series_name)
        load_to_motherduck(df, series_name)

    logger.info("BCB ingestion pipeline completed successfully")
