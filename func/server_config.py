from enum import IntEnum, Enum
from configparser import ConfigParser

def modify_configs(path, type, attr, value):
    path = "configs/" + path
    config = ConfigParser()
    config.read(path)
    config.set(type, attr, value)
    with open(path, "w") as configfile:
        config.write(configfile)

def init_configs(path):
    config_file = ConfigParser()
    config_file.read(path)
    settings = {}
    for section in config_file.sections():
        settings[section] = []
        for option in config_file.options(section):
            value = config_file.get(section, option)
            if value.lower() in ('true', 'false'):
                settings[section].append(config_file.getboolean(section, option))
            elif value.isdigit():
                settings[section].append(config_file.getint(section, option))
            elif value.startswith("0x"):
                settings[section].append(int(value, 16))
            else:
                settings[section].append(value)
    return settings
                    
class API_KEY(IntEnum):
    OPENAI_APIKEY = 0
    PYCAI_APIKEY = 1
    AZURE_KEY = 2
    
class PYCAI_SETTING(IntEnum):
    CREATOR_ID = 0
    CHAR_ID = 1
    CHAR_NAME = 2
    
class OPENAI_SETTING(IntEnum):
    MODEL = 0
    USER = 1

class AZURE_SETTING(IntEnum):
    ENDPOINT = 0
    LOCATION = 1

class DATA_PATH(IntEnum):
    DATABASE_CREATE = 0
    
class BOT_SETTING(IntEnum):
    STATUS = 0
    BOT_TOKEN = 1
    AVATAR_PATH = 2
    
class STYLE(IntEnum):
    EMBED_COLOR = 0
    
class PROGRAM_SETTING(IntEnum):
    SRC_TRANSLATE_MODE = 0
    DST_TRANSLATE_MODE = 1
    BOT_TRANSLATE_MODE = 2
    VOCAB = 3
    LANGUAGE = 4
    INDIVIDUAL_CHAT = 5
    CHANNEL_GROUP_CHAT = 6
    BOT_GROUP_CHAT = 7

#FOR PROGRAM
DEFINE_OOC_COUNT = 15

class CHAT_TYPE(IntEnum):
    GROUP = 0
    INDIVIDUAL = 1
    NOTIFY = 2
    BOT = 3

class TRANSLATE_MODE(IntEnum):
    GOOGLE = 0
    OPENAI = 1
    AZURE = 2

class GUILD(IntEnum):
    GUILD_ID = 0
    TASK_CHANNEL_ID = 1
    EVENT_CHANNEL_ID = 2
    NOTIFY_CHAT_ID = 3
    ACCESS = 4
    
class CHANNEL(IntEnum):
    CHANNEL_ID = 0
    GUILD_ID = 1
    GROUP_CHAT_ID = 2
    ACCESS = 3
    LAST_MESSAGE_ID = 4
    LAST_TURN_ID = 5

class INDIVIDUALS(IntEnum):
    USER_ID = 0
    USER_NAME = 1
    CHAT_ID = 2
    ACCESS = 3
    LAST_MESSAGE_ID = 4
    LAST_TURN_ID = 5
    
class MEMBERS(IntEnum):
    GUILD_ID = 0
    USER_ID = 1
    USER_NAME = 2
    ACCESS = 3
    
class ADMIN(IntEnum):
    USER_ID = 0
    PRIVILAGE = 1

class BOT(IntEnum):
    BOT_ID = 0
    BOT_NAME = 1
    CHARA_NAME = 2

class BOT_CHAT(IntEnum):
    BOT_ID = 0
    BOT_CHAT_ID = 1
    LAST_TURN_ID = 2
    CHANNEL_ID = 3
    STATE = 4
    LAST_MESSAGE_TEXT = 5
    
class EMBED_TYPE(IntEnum):
    NAME_PROCESSING = 0
    NAME_COMPLETE = 1
    NSFW_PROCESSING = 2
    NSFW_COMPLETE = 3
    CLEAN_COMPLETE = 4
    RESET_PROCESSING = 5
    RESET_COMPLETE = 6
    SHOW_INFO = 7
    SHOW_LIST = 8
    NSFW_FILTER = 9
    EXECUTED_FLAG = 10
    REMOVE_LAST_MESSAGE = 11
    REFRESH_LAST_MESSAGE = 12
    STATUS_COMPLETE = 13
    REBOOT_PROCESSING = 14
    REBOOT_COMPLETE = 15
    RP_PROCESSING = 16
    RP_COMPLETE = 17
    OOC_PROCESSING = 18
    OOC_COMPLETE = 19
    ADMIN_COMPLETE = 20
    CHECK_PRIVILAGE = 21
    SHOW_TASK = 22
    SHOW_EVENT = 23
    TASK_COMPLETE = 24
    EVENT_COMPLETE = 25
    TASK_EVENT_DISABLED = 26
    BOT_CHAT_EMBED = 27
    BOT_CHAT_DISABLED = 28
    DM_NOT_AVALIABLE = 29
    
    