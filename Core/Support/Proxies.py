import os
import random

class proxy:
    try:
        from Core.Support import Language
        Parser = Language.Translation.Parser
        Proxy_file = Parser["Settings"]["Proxy_List"]
    except Exception:
        Proxy_file = "None"

    Proxies_List = []
    if Proxy_file and str(Proxy_file).lower() != "none" and os.path.exists(str(Proxy_file)):
        try:
            with open(Proxy_file, "r") as file_obj:
                Proxies_List = [line.strip() for line in file_obj.readlines() if line.strip()]
        except Exception:
            Proxies_List = []

    final_proxis = Proxies_List
    chosen_proxy = random.choice(Proxies_List) if Proxies_List else ""
    choice3 = chosen_proxy
    choice = chosen_proxy
    choice2 = chosen_proxy
