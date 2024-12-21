import requests
import json
import time
import re
from tqdm import tqdm

input_file = "steam_games_descriptions.json"
output_file = "steam_games_dictionary.json"

# load descriptions
try:
    with open(input_file, "r") as file:
        descriptions = json.load(file)
except FileNotFoundError as e:
    print(f"Error loading the file {input_file}: {e}")
    exit()

word_count = {}

progress_bar = tqdm(descriptions, desc="Calculating dict", unit="game")

# iterate over each game description and add the words to the dictionary
for game, description in descriptions.items():
    # encode 
    description = description.encode("ascii", "ignore").decode()
    words = description.split()
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    progress_bar.update(1)

# sort the dictionary by value
word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))

# save the dictionary
with open(output_file, "w") as file:
    json.dump(word_count, file, indent=4)