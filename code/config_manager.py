import os
import json

global CONFIG
global FILE_TYPES
global CONFIG_FILE
global CONTENT_DIR

def get_config(config_file=CONFIG_FILE, content_dir=CONTENT_DIR):
    global CONFIG
    global CONFIG_FILE
    global CONTENT_DIR
    CONTENT_DIR = content_dir
    CONFIG_FILE = config_file
    #check if the config file exists if not create it
    if not os.path.exists(path=config_file):
        with open(file=config_file, mode='w') as outfile:
            json.dump(obj={}, fp=outfile)

    with open(file=config_file) as json_file:
        config = json.load(fp=json_file)
    CONFIG = config
    return config


def get_content_dir():
    return CONTENT_DIR

def update_config():
    for key in CONFIG:
        add_config_value(keyname=key, config_key=key)

def add_config_value(keyname, config_key):
    '''
    Adds a value to the config file
    '''
    if CONFIG is None:
        print("CONFIG is None, you need to run get_config before you can use this function")
        os.exit(0) 

    value = None
    if config_key not in CONFIG:
        while value is None or value == '':
            value = input(prompt=f"Please enter the value for {keyname}: ")
    else:
        value = input(prompt=f"Please enter the value for {keyname} ({CONFIG[config_key]}): ")

        CONFIG[config_key] = value
        with open(file=CONFIG_FILE, mode='w') as outfile:
            json.dump(obj=CONFIG, fp=outfile)
    return CONFIG[config_key]


def get_api_key():   
    '''
    Gets the api key from the config file
    '''
    if CONFIG is None:
        print("CONFIG is None, you need to run get_config before you can use this function")
        os.exit(0) 

    if 'openai_api_key' not in CONFIG:
        api_key = input(prompt="Please enter your openai api key: ")
        CONFIG['openai_api_key'] = api_key
        with open(file=CONFIG_FILE, mode='w') as outfile:
            json.dump(obj=CONFIG, fp=outfile)

    return CONFIG['openai_api_key']



def read_file_types():
    global FILE_TYPES
    if FILE_TYPES is not None:
        return FILE_TYPES
    file_types = {}
    #list all the dirs under filetypes
    dirs = os.listdir(path='filetypes')
    for dir in dirs:
        #read the file
        with open(file='filetypes/' + dir + '/filetype.json') as json_file:
            file_type = json.load(fp=json_file)
            file_types[file_type['name']] = file_type
    FILE_TYPES = file_types
    return file_types