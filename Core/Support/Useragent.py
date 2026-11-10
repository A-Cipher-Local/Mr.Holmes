import os
import random

class Select:
    try:
        from Core.Support import Language
        parser = Language.Translation.Parser
        useragent_file = parser["Settings"]["useragent_List"]
    except Exception:
        useragent_file = "None"

    value = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\n"]
    
    if useragent_file and str(useragent_file).lower() != "none" and os.path.exists(str(useragent_file)):
        try:
            with open(useragent_file, "r") as file_obj:
                lines = [line.strip() for line in file_obj.readlines() if line.strip()]
                if lines:
                    value = lines
        except Exception:
            pass

    agent = random.choice(value).replace("\n","")
