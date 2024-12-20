import requests
import json
import time
import re
from tqdm import tqdm


input_file = "steam_games_list.json"
output_file = "steam_games_descriptions.json"
failed_output_file = "failed_appids.json"

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
failed_appids = []
index_progress = 0

def save_progress():
    with open(output_file, "w") as file:
        json.dump(descriptions, file, indent=4)
    with open(failed_output_file, "w") as file:
        json.dump(failed_appids, file, indent=4)
    with open("index_" + failed_output_file, "w") as file:
        json.dump(index_progress, file, indent=4)


# base URL for API request
base_url = "https://store.steampowered.com/api/appdetails"

progress_bar = tqdm(data["applist"]["apps"], desc="Fetching game descriptions", unit="game")

# loop through games and fetch description
for index, app in enumerate(data["applist"]["apps"]):
    if index > 100: exit() #! DEBUG
    appid = app["appid"]
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
    except Exception as e:
        progress_bar.set_postfix({"Error": f"Failed appid {appid}: {e}"})
        failed_appids.append(appid)
    
    # save progress every N games
    if (index + 1) % 10 == 0:
        save_progress()
    
    progress_bar.update(1)
    index_progress = index

    # sleep to avoid overwhelming the API (max 100'000 requests per day)
    time.sleep(0.2)
    # time.sleep(100000/(24*60*60))

# save all at the end
save_progress()
print(f"Detailed descriptions saved to {output_file}")
