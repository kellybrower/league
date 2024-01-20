import os
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")
BASE_URL = "https://americas.api.riotgames.com/lol/"


# Function to read match IDs from a file
def read_match_ids_from_file():
    with open("match_ids.txt", "r") as file:
        return [line.strip() for line in file]


def get_match_info(match_id):
    """
    Fetch detailed information about a specific match.
    """
    url = f"{BASE_URL}match/v5/matches/{match_id}"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def create_match_performance_dataframe(match_info):
    """
    Create a DataFrame with match performance data.
    """
    data = []
    participants = match_info.get("info", {}).get("participants", [])
    for participant in participants:
        stats = participant.get("stats", {})
        match_id = match_info.get("metadata", {}).get("matchId")
        champion_id = participant.get("championId")
        kills = stats.get("kills")
        deaths = stats.get("deaths")
        assists = stats.get("assists")
        data.append([match_id, champion_id, kills, deaths, assists])

    columns = ["Match ID", "Champion ID", "Kills", "Deaths", "Assists"]
    return pd.DataFrame(data, columns=columns)


# Example usage
if __name__ == "__main__":
    # Read match IDs from the file
    match_ids = read_match_ids_from_file()
    performance_dataframes = []

    try:
        for match_id in match_ids:
            match_info = get_match_info(match_id)
            if match_info:
                performance_dataframe = create_match_performance_dataframe(match_info)
                performance_dataframes.append(performance_dataframe)
            else:
                print(f"Match {match_id} not found.")

        # Concatenate all DataFrames into a single DataFrame
        combined_dataframe = pd.concat(performance_dataframes, ignore_index=True)

        # Save the combined DataFrame to a CSV file
        return combined_dataframe