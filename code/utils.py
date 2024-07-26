import re

def array_to_string(array):

    #filter out duplicates case insensitive
    array = list(dict.fromkeys(array))

    if len(array) == 0:
        return ''
    elif len(array) == 1:
        return array[0]
    elif len(array) == 2:
        return ' and '.join(array)
    else:
        return ', '.join(array[:-1]) + ', and ' + array[-1]


PARSE_FILES = {}
def parse_file(filename, vars):
    '''
    read the file, store it in a global variable to save the file read in the future,
    then parse the key value pairs from vars into the file contents and return the results looking
    for the pattern {{keyname}} and replacing it with value
    '''
    global PARSE_FILES
    if filename in PARSE_FILES:
        file_contents = PARSE_FILES[filename]
    else:
        with open(filename, 'r') as file:
            file_contents = file.read()
        PARSE_FILES[filename] = file_contents
    
    for key, value in vars.items():
        file_contents = file_contents.replace('{{' + key + '}}', value)

    #replace any remaining variables with empty strings
    file_contents = re.sub(r'{{.*?}}', '', file_contents)

    return file_contents






def trim_whitespace(input_string):
    return re.sub(r'\s+', ' ', input_string)

def format_review(review):
    new_review = ""
    #convert review from json to object
    for key, value in review.items():
        new_review += key + ": \n" + str(value) + "\n\n"
    return new_review