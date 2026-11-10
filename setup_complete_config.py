import os
import configparser

config_dir = "Configuration"
os.makedirs(config_dir, exist_ok=True)
config_file = os.path.join(config_dir, "Configuration.ini")

config = configparser.ConfigParser()
config["Settings"] = {
    "api_key": "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",
    "Show_Logs": "True",
    "ProxyLoc": "None",
    "language": "English",
    "Proxy_List": "None"
}

with open(config_file, "w") as f:
    config.write(f)

print("[+] Successfully generated complete Configuration.ini with all required keys!")
