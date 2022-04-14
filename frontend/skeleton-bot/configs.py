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

with open("frontend/skeleton-bot/angular.json", "r") as file:
    ang = json.load(file)

with open("configs/config.json", "r") as file:
    configs = json.load(file)

ang["projects"]["skeleton-bot"]["architect"]["serve"]["options"]["port"] = configs["frontPort"]

with open("frontend/skeleton-bot/angular.json", "w") as file:
    json.dump(ang, file, indent=4)