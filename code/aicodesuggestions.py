import openai
import json
import os
import sys
import argparse
import requests
import json
import time
import random
import string
import re
import datetime
import logging
import traceback
import uuid
import base64
import hashlib
import pprint



#globals
PROMPT_BEGIN = os.environ.get('PROMPT_BEGIN', 'Riddle me this Batman: ')
CONFIG_FILE = "~/.ssh/aidocumentor_config.json"


FILE_TYPES = {
    'python' : {
        'extensions' : ['py'],
        'expertise' : ['python'],
        'role': ['Senior Software Engineer']
    }
}


def get_config():
    #check if the config file exists if not create it
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as outfile:
            json.dump({}, outfile)

    with open(CONFIG_FILE) as json_file:
        config = json.load(json_file)
    return config

def get_api_key():
    '''
    Gets the api key from the config file
    '''
    config = get_config()
    return config['openai_api_key']

def send_prompt(prompt):
    '''
    Sends the prompt to the openai api
    '''
    '''
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        temperature=0.9,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    '''

    model="gpt-3.5-turbo-0613"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt }
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
        #functions=functions,
        #function_call="auto"  # auto is default, but we'll be explicit
    )


    #this is for troubleshooting
    myresponse = response
    mycontent = myresponse['choices'][0]['message']['content']
    #convert myresponse to an object, delete the choices array, and then convert back to json
    myresponse = json.loads(json.dumps(myresponse))
    del myresponse['choices']
    myresponse = json.dumps(myresponse)
    #print (myresponse)
    #print (mycontent)

    return response


def list_files():
    '''
    Lists the files in the current in /app/data
    '''
    files = os.listdir('/app/data')
    return files




def get_file_contents(filename):
    '''
    Gets the contents of the file
    '''
    with open('/app/data/' + filename, 'r') as file:
        data = file.read()
    return data


def get_file_type(filename):
    '''
    Gets the file type based on the extension
    '''
    file_type = None
    for key, value in FILE_TYPES.items():
        if filename.endswith(tuple(value['extensions'])):
            file_type = key
            break
    return file_type


def get_functions(filename):
    '''
    Gets the functions from the python file
    '''
    file_type = get_file_type(filename)

    if not file_type:
        return "Unknown file type"
    elif file_type == 'python':
        #get the contents of the file
        contents = get_file_contents(filename)

        #get the functions
        functions = re.findall(r'def\s+([a-zA-Z0-9_]+)\s*\(', contents)

        return functions
    


def get_function_by_name(filename, function_name):

    #get the file type based on the extension
    file_type = get_file_type(filename)

    if not file_type:
        return "Unknown file type"
    elif file_type == 'python':
        # Get the contents of the file
        contents = get_file_contents(filename)

        # Find the entire function definition using regex
        pattern = r'def\s+' + function_name + r'\s*\((.*?)\):([\s\S]*?)(?=def|\Z)'
        function_matches = re.findall(pattern, contents, re.DOTALL)

        lines = function_matches[0][1].strip()

        # Check if any matches were found
        if function_matches:
            return { 'args' : function_matches[0][0], 'lines' : lines }

        return None, None



'''
FILE_TYPES = {
    'python' : {
        'extensions' : ['py'],
        'expertise' : ['python'],
        'role': ['Senior Software Engineer']
    }
}
'''


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



def review_function(filename, function_name):
    #get the function
    function = get_function_by_name(filename, function_name)


    type_details = FILE_TYPES[get_file_type(filename)]

    #lines = function['lines']

    #TODO: add expertise from the file contents too


    role_array = type_details['role']
    expertise_array = type_details['expertise']



    #get the prompt
    prompt = (
        "You are a " + array_to_string(role_array) + 
        " with expertise in " + array_to_string(expertise_array) +
        " and you are reviewing a function called " + function_name + " in a " + get_file_type(filename) + " file." + 
        " The function takes " + function['args'] + " as arguments and does the following: " + 
        "\n\n```\n\n" + function['lines'] + "\n\n```\n\n" +
        " You are reviewing the function to make sure it is correct. "  +
        " You should return a json object with your response (it is very important that this be valid json). " +
        " Where you give a score from 1 to 10 for the function in how well it's written" +
        " and a comment on what could be improved." +
        " The score should be based on the following criteria: " +
        " 1. Does the function do what it's supposed to do? " +
        " 2. Is the function easy to read? " +
        " 3. Is the function easy to understand? " +
        " 4. Is the function easy to maintain? " +
        " 5. Is the function easy to test? " +
        " 6. Is the function easy to debug? " +
        " 7. Is the function easy to extend? " +
        " 8. Is the function easy to reuse? " +
        " 9. Is the function easy to refactor? " +
        " 10. Is the function easy to document? " +
        " 11. Is the function easy to deploy? " +
        " 12. Is the function easy to scale? " +
        " 13. Is the function easy to secure? " +
        " 14. Is the function easy to monitor? " +
        " 15. Is the function easy to optimize? " +
        " 16. Is the function easy to profile? " +
        " 17. Is the function easy to cache? " +
        " 18. Is the function easy to load test? " +
        " 19. Is the function easy to mock? " +
        " 20. Is the function easy to stub? " +
        " \n\n" +
        " You will also give a short description of the function and what it does, keep it susinct as possible. " + " \n\n" +
        " You will also give a long description of the function and what it does, with lots of details to help someone who is reviewing the code know everything happening inside it. " + " \n\n" +
        " You will also give a list of the things that could be improved in the function. " + " \n\n" +
        " You will also give a list of any external files used by the function. " + " \n\n" +
        " If the function requires expertise in any domain other than " + array_to_string(expertise_array) + " then you should mention that in your review. " + " \n\n" +
        " If the function uses any other functions from the same file list them, the current file has these functions: " + array_to_string(get_functions(filename)) + " \n\n" +
        " an example review is: " + " \n\n" +
        " { " +
        '   "score": 8, ' +
        '   "score_reasons": "function only scored a 7 in readability, changing the varaible x to be contextual would make it more readable", ' +
        '   "comment": "This function is perfect", ' +
        '   "short_description": "Do the thing", ' +
        '   "long_description": "This function function does a cool thing wich uses aws and file systems, it takes your zazzlefratz and turns it into a quisbit", ' +
        '   "improvements": "This function is nearly perfect, just rename that variable", ' +
        '   "other_functions": "list_tasks, get_pictures, and do_this_thing", ' +
        '   "external_files": "config.json and file from variable MY_FILE", ' +
        '   "expertise": "aws, os, filesystems", ' +
        " } " 

    )

    #send the prompt
    return  send_prompt(prompt)

def trim_whitespace(input_string):
    return re.sub(r'\s+', ' ', input_string)

def format_review(review):
    new_review = ""

    # Replace actual newlines and tabs with escape sequences within double quotes
    #review = re.sub(r'"([^"]*)\n([^"]*)"', r'"\1\\n\2"', review)
    #review = re.sub(r'"([^"]*)\t([^"]*)"', r'"\1\\t\2"', review)
    #review = review.replace('\n', '\\n').replace('\t', '\\t')

    #print("converting review to json: " + review)

    #converrt review from json to object
    for key, value in review.items():
        new_review += key + ": \n" + str(value) + "\n\n"
    return new_review
    #return review



def get_review_as_comment(filename, function_name):
    type = get_file_type(filename)
    hash = hash_the_function(filename, function_name)


    if check_comment_hash(filename, function_name, hash):
        return "Already reviewed this function"

    review = fetch_review(filename, function_name)


    if review is None:
        return ""
    else:
        new_review = "''' \n" 
        new_review = new_review + hash + ":" + filename + ":" + function_name + " -----Automated Review Start------\n" 
        new_review = new_review + format_review(review) 
        new_review = new_review + " \n" + hash + ":" + filename + ":" + function_name + " -----Automated Review End-----\n" 
        new_review = new_review + "''' \n"
        return new_review

import json
import requests

def fetch_review(filename, function_name, max_retries=10):
    for _ in range(max_retries):
        review = review_function(filename, function_name)  # Replace with your actual code to fetch the review
        
        try:
            #review_str = str(review)
            review_str = str(review['choices'][0]['message']['content'])
            review_json = json.loads(review_str )
            return review_json  # Return the JSON object if parsing is successful
        except json.JSONDecodeError:
            # Parsing failed, retry
            continue
    
    return None  # Return None if all retries failed

def hash_the_function(filename, function_name):
    type = get_file_type(filename)
    hash = ''
    if type == 'python':
        function = get_function_by_name(filename, function_name)
        lines = function['lines']
        #hash the lines to see if they have changed
        hash_object = hashlib.md5(lines.encode())
        hash = hash_object.hexdigest()
        return hash
    else:
        return 'file type unknown'

def check_comment_hash(filename, function_name, hash):
    type = get_file_type(filename)
    hash = hash_the_function(filename, function_name)
    if type == 'python':
        contents = get_file_contents(filename)
        pattern = hash + ":" + filename + ":" + function_name
        matches = re.findall(pattern, contents)
        if len(matches) > 0:
            return True
        else:
            return False
    else:
        return False




def read_special_comment_block(function_name, filename):
    """
    Reads the special comment block associated with a function from the file.

    Args:
        function_name (str): The name of the function.
        file_path (str): The path to the file.

    Returns:
        dict: A dictionary containing the extracted key-value pairs from the comment block.
    """
    file_path = '/app/data/' + filename
    with open(file_path, 'r') as file:
        content = file.read()

    #print("matching for function: " + function_name + " in file: " + filename)
    pattern = r"'''([\s\S]*?:{}:{}\s-----Automated Review Start-----)(.*?)-----Automated Review End-----[\s\S]'''".format(re.escape(filename), re.escape(function_name))

    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        comment_block = match.group(2).strip()
        lines = comment_block.split('\n')
        comment_dict = {}

        value = ''
        key = ''
        for line in lines:
            #print("------\n" + line)
            if ':' not in line and key != '':
                value += line + '\n'
            elif ':' in line:
                if key != '':
                    comment_dict[key.strip()] = value.strip()
                key, empty = line.split(':', 1)
                value = ''

        if key != '':
            comment_dict[key.strip()] = value.strip()
            
        return comment_dict
    else:
        return None




def update_special_comment_block(function_name, filename, new_comment_block, checkfunctions=True):
    """
    Updates or inserts the special comment block associated with a function in the file.

    Args:
        function_name (str): The name of the function.
        file_path (str): The path to the file.
        new_comment_block (str): The new comment block to replace or insert.
    """

    file_contents = None
    function_list = None
    if checkfunctions:
        file_contents = get_file_contents(filename)
        function_list = get_functions(filename)

    if new_comment_block == 'Already reviewed this function':
        return 'No update to comment, already reviewed this function'
    else:
        current_comments = read_special_comment_block(function_name, filename)

        file_path = '/app/data/' + filename

        if current_comments is not None:
            print("found a comment to replace")
            with open(file_path, 'r') as file:
                content = file.read()

            pattern = r"'''([\s\S]*?:{}:{}\s-----Automated Review Start-----)(.*?)-----Automated Review End-----[\s\S]'''".format(re.escape(filename), re.escape(function_name))

            match = re.search(pattern, content, re.DOTALL)
    
            if not match:
                print("something went wrong, the comment block was not found")
                return 'Comment not found'


            def replace_comment(match):
                return new_comment_block

            updated_content = re.sub(pattern, replace_comment, content, flags=re.DOTALL)

            if updated_content == content:
                print("the comment was not replaced for some reason, this is bad")
                return 'Comment not replaced'



            with open(file_path, 'w') as file:
                file.write(updated_content)


            if checkfunctions:
                check_function_list = get_functions(filename)
                if function_list == check_function_list:
                    return 'Updated comment'
                else:
                    print("Something went horribly wrong, the functions in the file changed while reviewing them")
                    with open('/app/data/' + filename, 'w') as file:
                        file.write(file_contents)
                    return 'we ate a function, putting everything back'

        else:
            print("no comment found, inserting new comment")
            inserted = insert_comment_before_function(file_path, function_name, new_comment_block)

            if checkfunctions:
                check_function_list = get_functions(filename)
                if function_list == check_function_list:
                    if inserted:
                        return 'Inserted comment'
                    else:
                        return 'Function not found'
                else:
                    print("Something went horribly wrong, the functions in the file changed while reviewing them")
                    with open('/app/data/' + filename, 'w') as file:
                        file.write(file_contents)
                    return 'we ate a function, putting everything back'
    return 'Something went wrong with update_special_comment_block, you should never see this'





def insert_comment_before_function(file_path, function_name, new_comment):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line number of the function's definition
    function_line = None
    for i, line in enumerate(lines):
        if f'def {function_name}(' in line:
            function_line = i
            break

    print (function_name + " is at line " + str(function_line))

    # If the function was found, insert the new comment before it
    if function_line is not None:
        lines.insert(function_line, new_comment + '\n')

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)

        return True  # Insertion successful
    else:
        return False  # Function not found



def find_hash_value(file_contents, filename, function_name):
    search_pattern = r"{}:{}[\s\S]-----Automated Review Start-----".format(re.escape(filename), re.escape(function_name))

    lines = file_contents.split('\n')

    for line in lines:
        match = re.search(search_pattern, line)
        if match:
            print("found match while looking for the hash")
            return line.split(':')[0]

    return None



def remove_specialcomments_from_file(content, filename, function_name):

    pattern = r"'''([\s\S]*?:{}:{}\s-----Automated Review Start-----)(.*?)-----Automated Review End-----[\s\S]'''".format(re.escape(filename), re.escape(function_name))

    def replace_comment(match):
        return new_comment_block

    updated_content = re.sub(pattern, '', content, flags=re.DOTALL)

    return updated_content


def clean_up_mult_newlines(content):
    import re

    # Replace lines with only whitespace with a single newline
    content = re.sub(r'^[ \t]+$', '\n', content, flags=re.MULTILINE)

    # Replace consecutive newlines with just two newlines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content


def create_check_doc(content, filename, function_list):
    for function_name in function_list:
        content = remove_specialcomments_from_file(content, filename, function_name)
    content = clean_up_mult_newlines(content)
    return content

def review_doc(filename):
    function_status = {}
    file_contents = get_file_contents(filename)
    function_list = get_functions(filename)
    orig_file_contents = file_contents

    #review the functions
    for function_name in function_list:
        print("Reviewing function: " + filename + ":" + function_name)
        function_status[function_name] = update_special_comment_block(function_name, filename, get_review_as_comment(filename, function_name), checkfunctions=True)
        print("Review complete: " + function_name + " status: " + function_status[function_name])

    #get the results to verify it all worked right
    after_file_contents = get_file_contents(filename)
    after_function_list = get_functions(filename)


    #compare function_list and check_function_list
    if create_check_doc(file_contents, filename, function_list) == create_check_doc(after_file_contents,filename, function_list) and function_list == after_function_list:
        #fix any whitespace issues
        with open('/app/data/' + filename, 'w') as file:
            file.write(clean_up_mult_newlines(after_file_contents))
        print("All functions reviewed and new lines cleaned up")
        return function_status
    else:
        print("Something went horribly wrong, the functions in the file changed while reviewing them")
        #write file_contents back to the file
        with open('/app/data/' + filename, 'w') as file:
            file.write(orig_file_contents)

        with open('/app/data/' + filename + '.bad_doc_review', 'w') as file:
            file.write(create_check_doc(after_file_contents,filename, function_list))

        with open('/app/data/' + filename + '.pre_bad_doc_review', 'w') as file:
            file.write(create_check_doc(orig_file_contents,filename, function_list))
        
        
               
        
        
       

        return {}





def help():
    print("This AI tool can look at the current directory and answer questions or do updates")
    print("Commands are: ")
    print("     help - prints this help message")
    print("     list - lists the files in the current directory")
    print("     review_doc <filename> - reviews all the functions in the file and updates the special comment blocks")
    print("     review_docs - reviews all the functions in all the files in the current directory and updates the special comment blocks")



def main():
    #check that there is an ai key in the config if not ask for one and update it
    config = get_config()
    if 'openai_api_key' not in config:
        api_key = input("Please enter your openai api key: ")
        config['openai_api_key'] = api_key
        with open('config.json', 'w') as outfile:
            json.dump(config, outfile)

    #get the api key
    api_key = get_api_key()
    openai.api_key = api_key




    #if there is no args then run help and exit
    if len(sys.argv) == 1:
        help()
        exit()
    else: 
        #if there is an arg then run the command
        command = sys.argv[1]
        if command == 'help':
            help()
        elif command == 'list':
            files = list_files()
            print(files)
        elif command == 'functions':
            filename = sys.argv[2]
            functions = get_functions(filename)
            print(functions)
        elif command == 'function':
            filename = sys.argv[2]
            function_name = sys.argv[3]
            function = get_function_by_name(filename, function_name)
            #print the formatted function results
            print("Function: " + function_name)
            print("Args: " + function['args'])
            print("Lines: " + function['lines'])
        elif command == 'review_function':
            filename = sys.argv[2]
            function_name = sys.argv[3]
            review = get_review_as_comment(filename, function_name)
            print(review)
        elif command == 'get_comments':
            filename = sys.argv[2]
            function_name = sys.argv[3]
            comment_dict = read_special_comment_block(function_name, filename)
            if comment_dict:
                for key, value in comment_dict.items():
                    print(f"{key}: {value}")
            else:
                print("Special comment block not found.")
        elif command == 'update_comments':
            filename = sys.argv[2]
            function_name = sys.argv[3]
            print(update_special_comment_block(function_name, filename, get_review_as_comment(filename, function_name)))
        elif command == 'remove_review':
            filename = sys.argv[2]
            function_name = sys.argv[3]
            #file_contents = get_file_contents(filename)
            #new_file_contents = remove_specialcomments_from_file(file_contents, filename, function_name)
            #with open('/app/data/' + filename, 'w') as file:
            #    file.write(new_file_contents)
            #def update_special_comment_block(function_name, filename, new_comment_block, checkfunctions=True):
            print(update_special_comment_block(function_name, filename, ' ', checkfunctions=False))

            print("Review removed")
        elif command == 'review_doc':
            filename = sys.argv[2]
            print(review_doc(filename))
        elif command == 'check_doc':
            filename = sys.argv[2]
            function_list = get_functions(filename)
            file_contents = get_file_contents(filename)
            with open('/app/data/' + filename + '.check_doc', 'w') as file:
                file.write(create_check_doc(file_contents, filename, function_list))
            print ("check doc created as " + filename + ".check_doc")
        elif command == 'review_docs':
            files = list_files()
            for filename in files:
                if filename.endswith(tuple(FILE_TYPES['python']['extensions'])):
                    print("Reviewing file: " + filename)
                    review_doc(filename)
            print("Review complete")
        else:
            print("Unknown command: " + command)
            help()
            exit()






    
main()