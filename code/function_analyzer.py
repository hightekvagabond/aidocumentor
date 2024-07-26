import re
import hashlib
from file_operations import get_file_contents, get_file_type
from config_manager import read_file_types, get_content_dir



def get_functions(filename):
    '''
    Gets the functions from the python file
    '''
    file_types = read_file_types()

    content_dir = get_content_dir()

    file_type = get_file_type(filename=filename,file_types=file_types)

    if not file_type:
        return "Unknown file type"
    elif file_type == 'python':
        #get the contents of the file
        contents = get_file_contents(content_dir=content_dir, filename=filename)

        #get the functions
        functions = re.findall(pattern=r'def\s+([a-zA-Z0-9_]+)\s*\(', string=contents)

        return functions


def get_function_by_name(filename, function_name):

    file_types = read_file_types()
    content_dir = get_content_dir()

    #get the file type based on the extension
    file_type = get_file_type(filename=filename,file_types=file_types)

    if not file_type:
        return "Unknown file type"
    elif file_type == 'python':
        # Get the contents of the file
        contents = get_file_contents(content_dir=content_dir, filename=filename)

        # Find the entire function definition using regex
        pattern = r'def\s+' + function_name + r'\s*\((.*?)\):([\s\S]*?)(?=def|\Z)'
        function_matches = re.findall(pattern=pattern, string=contents, flags=re.DOTALL)

        lines = function_matches[0][1].strip()

        # Check if any matches were found
        if function_matches:
            return { 'args' : function_matches[0][0], 'lines' : lines }

        return None, None

def hash_the_function(filename, function_name, file_types):
    type = get_file_type(filename=filename,file_types=file_types)
    hash = ''
    if type == 'python':
        function = get_function_by_name(filename=filename, function_name=function_name)
        lines = function['lines']
        #hash the lines to see if they have changed
        hash_object = hashlib.md5(string=lines.encode())
        hash = hash_object.hexdigest()
        return hash
    else:
        return 'file type unknown'