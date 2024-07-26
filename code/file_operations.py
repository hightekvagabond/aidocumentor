import os

from config_manager import get_content_dir, read_file_types

def list_files():
    '''
    Lists the files in the current in CONTENT_DIR
    '''
    content_dir = get_content_dir()
    files = os.listdir(content_dir)
    return files


def get_file_contents(filename):
    '''
    Gets the contents of the file
    '''
    content_dir = get_content_dir()
    with open( file=content_dir + '/' + filename, mode='r') as file:
        data = file.read()
    return data


def get_file_type(filename):
    '''
    Gets the file type based on the extension
    '''
    file_types = read_file_types()
    file_type = None
    for key, value in file_types.items():
        if filename.endswith(tuple(iterable=value['extensions'])):
            file_type = key
            break
    return file_type