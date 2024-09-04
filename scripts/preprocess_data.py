import json
import os
from typing import Dict, List
import pandas as pd
import requests

JSON_URL = "https://climatereanalyzer.org/clim/t2_daily/json/era5_world_t2_day.json"
JSON_PATH = "./data/raw/era5_world_t2_day.json"

def download_json(url: str, save_path: str) -> None:
    """
    Downloads a JSON file from the given URL and saves it to the specified path.

    Args:
        url (str): The URL of the JSON file to download.
        save_path (str): The path where the downloaded JSON file will be saved.

    Raises:
        requests.RequestException: If there's an error during the download process.
        IOError: If there's an error saving the file.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'w') as file:
            json.dump(response.json(), file)
        print(f"JSON file successfully downloaded and saved to {save_path}")
    except requests.RequestException as e:
        raise requests.RequestException(f"Error downloading the JSON file: {e}")
    except IOError as e:
        raise IOError(f"Error saving the JSON file: {e}")

def analyze_max_temperatures(json_file_path: str) -> pd.DataFrame:
    """
    Analyzes the maximum temperatures from a JSON file.

    Args:
        json_file_path (str): The file path to the JSON file containing temperature data.

    Returns:
        pd.DataFrame: A DataFrame containing the maximum temperatures for each year.

    Raises:
        FileNotFoundError: If the specified JSON file is not found.
        json.JSONDecodeError: If the JSON file is not properly formatted.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {json_file_path} was not found.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"The file {json_file_path} is not a valid JSON file.")

    max_temperatures: Dict[int, float] = {}
    exclude_series: List[str] = ["1979-2000", "1981-2010", "1991-2020"]

    for item in data:
        year = item['name']
        if year not in exclude_series:
            try:
                year_int = int(year)
                temperatures = [t for t in item['data'] if t is not None]
                if temperatures:
                    max_temperatures[year_int] = max(temperatures)
            except ValueError:
                print(f"Ignoring non-year entry: {year}")

    df = pd.DataFrame.from_dict(max_temperatures, orient='index', columns=['Max Temperature'])
    df.index.name = 'Year'
    return df.sort_index()

def main() -> None:
    """
    Main function to download the JSON data, process it, and save it to a CSV file.
    """
    try:
        download_json(JSON_URL, JSON_PATH)
        df = analyze_max_temperatures(JSON_PATH)
        df.to_csv('./data/processed/processed_data.csv')
        print("Data processing completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()