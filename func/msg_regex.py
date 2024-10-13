import re
import opencc
import configparser
    
class MSG_REGEX():
    
    def __init__(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        self.PROPER_TW_HUMAN_NAME = config["PROPER_TW_HUMAN_NAME"]
        self.PROPER_TW_PROPER_NOUN = config["PROPER_TW_PROPER_NOUN"]
        self.PROPER_EN_HUMAN_NAME = config["PROPER_EN_HUMAN_NAME"]
        self.PROPER_EN_PROPER_NOUN = config["PROPER_EN_PROPER_NOUN"]
        
    def msg_adjust_TW(self, text: str):
        converted_text = ""
        
        for split in text.split("\n"):
            for key, value in self.PROPER_EN_HUMAN_NAME.items():
                split = re.sub(value, key, split)
            for key, value in self.PROPER_EN_PROPER_NOUN.items():
                split = re.sub(value, key, split)
            converted_text += f"{split}\n"
            
        converted_text = converted_text.rstrip("\n")
        return converted_text
            
    def msg_adjust_EN(self, text: str):
        converted_text = ""
        
        for split in text.split("\n"):
            for key, value in self.PROPER_TW_HUMAN_NAME.items():
                split = re.sub(value, key, split)
            for key, value in self.PROPER_TW_PROPER_NOUN.items():
                split = re.sub(value, key, split)
            converted_text += f"{split}\n"
        
        converted_text = converted_text.rstrip("\n")
        return converted_text

def remove_mentions(text, bot_name):
    text = re.sub(f"(@{bot_name})", "", text)
    return text

def convert_to_TW(text: str):
    converter = opencc.OpenCC('s2t.json')
    text = converter.convert(text)
    return text

def clean_string(text: str):
    cleaned_string = re.sub(r'^[（(:oocOOC:：]+', '', text)
    cleaned_string = re.sub(r'[）):：]+$', '', cleaned_string)

    return cleaned_string

def remove_ooc(text:str):
    pattern = r'\([^)]*\)|（[^）]*）'
    result_string = re.sub(pattern, '', text)
    
    return result_string

        
    