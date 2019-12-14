import json

def get_config(guild_id):
    config = {"ERROR": 0, "GUILD_ID": guild_id}
    file_name = str(guild_id) + ".json"
    try:
        fin = open("./data/" + file_name, 'r')
    except FileNotFoundError:
        config["ERROR"] = -1
    else:
        config = json.load(fin)

    return config

def save_config(config):
    if isinstance(config, dict):
        fin = open("./data/" + str(config["GUILD_ID"]) + ".json", 'w')
        json.dump(config, fin, indent = 4)