import requests
import json
import time
import re
from tqdm import tqdm


input_file = "steam_games_list.json"
output_file = "steam_games_descriptions.json"
discarded_output_file = "discarded_appids.json"

def beautify(text):
    # remove HTML tags
    text = re.sub(r"<[^>]*>", "", text)
    # remove newlines and extra spaces
    text = re.sub(r"\s+", " ", text)
    # convert utf-8 to ascii
    text = text.encode("ascii", "ignore").decode()
    # remove interpunction
    text = re.sub(r"[^\w\s]", "", text)
    # All lowercase
    text = text.lower()

    return text.strip()

# load games list
try:
    with open(input_file, "r") as file:
        data = json.load(file)
except FileNotFoundError as e:
    print(f"Error loading the file {input_file}: {e}")
    exit()

# result dictionary to store the descriptions
descriptions = {}
discarded_appids = []

def save_progress():
    with open(output_file, "w") as file:
        json.dump(descriptions, file, indent=4)
    with open(discarded_output_file, "w") as file:
        json.dump(discarded_appids, file, indent=4)


# load progress if the output file already exists
try:
    with open(output_file, "r") as file:
        descriptions = json.load(file)
except FileNotFoundError:
    pass

# load failed appids if the file exists
try:
    with open(discarded_output_file, "r") as file:
        discarded_appids = json.load(file)
except FileNotFoundError:
    pass

# base URL for API request
base_url = "https://store.steampowered.com/api/appdetails"

progress_bar = tqdm(data["applist"]["apps"], desc="Fetching game descriptions", unit="game")

# loop through games and fetch description
for index, app in enumerate(data["applist"]["apps"]):
    appid = app["appid"]

    # skip if already fetched
    if str(appid) in descriptions or str(appid) in discarded_appids:
        progress_bar.update(1)
        continue

    try:
        # make API request
        response = requests.get(base_url, params={"appids": appid})
        if response.status_code == 200:
            app_data = response.json()
            # check if successful
            if str(appid) in app_data and app_data[str(appid)]["success"]:
                detailed_description = app_data[str(appid)]["data"].get("detailed_description", "")
                detailed_description = beautify(detailed_description) # clean up the text
                if(len(detailed_description) > 0):  # only save if description is not empty
                    descriptions[appid] = detailed_description
        if descriptions.get(appid) is None:
            progress_bar.set_postfix({"Error": f"Discarded appid {appid}: No data found"})
            discarded_appids.append(appid)
    except Exception as e:
        progress_bar.set_postfix({"Error": f"Failed appid {appid}: {e}"})
    
    # save progress every N games
    if (index + 1) % 100 == 0:
        save_progress()
    
    progress_bar.update(1)

    # sleep to avoid overwhelming the API (max 100'000 requests per day) 
    #! any requests need at least 100ms between them
    time.sleep(100000/(24*60*60))

# save all at the end
save_progress()
print(f"Detailed descriptions saved to {output_file}")
