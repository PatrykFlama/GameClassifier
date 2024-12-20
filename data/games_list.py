import requests
import json

url = "https://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json"

response = requests.get(url)

if response.status_code == 200:
    # parse the json data
    data = response.json()
    
    output_file = "steam_games_list.json"
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)
    
    print(f"Success")
else:
    print(f"Failed: {response.status_code}")
