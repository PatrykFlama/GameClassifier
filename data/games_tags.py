import requests
import json
import time
from tqdm import tqdm

input_file = "steam_games_list.json"
output_file = "steam_games_tags_and_genres.json"
discarded_output_file = "discarded_appids_tags_and_genres.json"

# load games
try:
    with open(input_file, "r") as file:
        data = json.load(file)
except FileNotFoundError as e:
    print(f"Error loading the file {input_file}: {e}")
    exit()

# dict for res
game_tags_and_genres = {}
discarded_appids = []

def save_progress():
    with open(output_file, "w") as file:
        json.dump(game_tags_and_genres, file, indent=4)
    with open(discarded_output_file, "w") as file:
        json.dump(discarded_appids, file, indent=4)

# SteamSpy API URL
steamspy_base_url = "https://steamspy.com/api.php"

# load progress if the output file already exists
try:
    with open(output_file, "r") as file:
        game_tags_and_genres = json.load(file)
except FileNotFoundError:
    pass

# load failed appids if the file exists
try:
    with open(discarded_output_file, "r") as file:
        discarded_appids = json.load(file)
except FileNotFoundError:
    pass

progress_bar = tqdm(data["applist"]["apps"], desc="Fetching game tags and genres", unit="game")

def fetch_steamspy_data(appid):
    try:
        response = requests.get(steamspy_base_url, params={"request": "appdetails", "appid": appid})
        if response.status_code == 200:
            app_data = response.json()
            # check if data exists
            if "appid" in app_data and app_data["appid"] == appid:
                tags = app_data.get("tags", {})
                genre = app_data.get("genre", "")

                if tags != [] or genre != "":
                    return tags, genre
        
        progress_bar.set_postfix({"Error": f"Discarded appid {appid}: No data found"})
        discarded_appids.append(appid)

        return None, None
    except Exception as e:
        progress_bar.set_postfix({"Error": f"Failed appid {appid}: {e}"})
        return None, None


# for each game get tags and genre
for index, app in enumerate(progress_bar):
    appid = app["appid"]

    # skip processed games
    if str(appid) in game_tags_and_genres or str(appid) in discarded_appids:
        progress_bar.update(1)
        continue

    tags, genre = fetch_steamspy_data(appid)

    if tags is not None and genre is not None:
        game_tags_and_genres[appid] = {
            "tags": tags,
            "genre": genre
        }

    # save progress after every 100 games
    if (index + 1) % 100 == 0:
        save_progress()

    progress_bar.update(1)

    time.sleep(1)

# final save
save_progress()
progress_bar.close()
print(f"Tags and genres saved successfully to {output_file}")
print(f"Failed appids saved to {discarded_output_file}")
