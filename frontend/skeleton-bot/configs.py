import sys
import json

with open("frontend/skeleton-bot/extraConfigs.json", "r") as file:
    data = json.load(file)

try:
    https = sys.argv[1].lower() == "true" if len(sys.argv) > 1 else False
except ValueError:
    https = False

data['https'] = https

with open("frontend/skeleton-bot/extraConfigs.json", "w") as file:
    json.dump(data, file)
