import re


from file_operations import get_file_contents, get_file_type, get_file_contents, get_file_type, get_file_type
from function_analyzer import hash_the_function, get_functions 
from ai_interface import fetch_review
from utils import format_review
from config_manager import get_content_dir





def get_review_as_comment(filename, function_name):
    type = get_file_type(filename=filename)
    hash = hash_the_function(filename=filename, function_name=function_name)

    if check_comment_hash(filename=filename, function_name=function_name, hash=hash):
        return "Already reviewed this function"

    review = fetch_review(filename=filename, function_name=function_name)

    if review is None:
        return ""
    else:
        new_review = "''' \n" 
        new_review = new_review + hash + ":" + filename + ":" + function_name + " -----Automated Review Start------\n" 
        new_review = new_review + format_review(review=review) 
        new_review = new_review + " \n" + hash + ":" + filename + ":" + function_name + " -----Automated Review End-----\n" 
        new_review = new_review + "''' \n"
        return new_review



def read_special_comment_block(function_name, filename):
    """
    Reads the special comment block associated with a function from the file.

    Args:
        function_name (str): The name of the function.
        file_path (str): The path to the file.

    Returns:
        dict: A dictionary containing the extracted key-value pairs from the comment block.
    """
    content_dir = get_content_dir()
    file_path = content_dir + '/'  + filename
    with open(file=file_path, mode='r') as file:
        content = file.read()

    #print("matching for function: " + function_name + " in file: " + filename)
    pattern = r"'''([\s\S]*?:{}:{}\s-----Automated Review Start-----)(.*?)-----Automated Review End-----[\s\S]'''".format(re.escape(filename), re.escape(function_name))

    match = re.search(pattern=pattern, string=content, flags=re.DOTALL)
    
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


    content_dir = get_content_dir()
    file_contents = None
    function_list = None
    if checkfunctions:
        file_contents = get_file_contents(filename=filename)
        function_list = get_functions(filename)

    if new_comment_block == 'Already reviewed this function':
        return 'No update to comment, already reviewed this function'
    else:
        current_comments = read_special_comment_block(function_name=function_name, filename=filename)

        file_path = content_dir + '/'  + filename

        if current_comments is not None:
            print("found a comment to replace")
            with open(file=file_path, mode='r') as file:
                content = file.read()

            pattern = r"'''([\s\S]*?:{}:{}\s-----Automated Review Start-----)(.*?)-----Automated Review End-----[\s\S]'''".format(re.escape(pattern=filename), re.escape(pattern=function_name))

            match = re.search(pattern=pattern, string=content, flags=re.DOTALL)
    
            if not match:
                print("something went wrong, the comment block was not found")
                return 'Comment not found'


            def replace_comment(match):
                return new_comment_block

            updated_content = re.sub(pattern=pattern, repl=replace_comment, string=content, flags=re.DOTALL)

            if updated_content == content:
                print("the comment was not replaced for some reason, this is bad")
                return 'Comment not replaced'



            with open(file=file_path, mode='w') as file:
                file.write(updated_content)


            if checkfunctions:
                check_function_list = get_functions(filename=filename)
                if function_list == check_function_list:
                    return 'Updated comment'
                else:
                    print("Something went horribly wrong, the functions in the file changed while reviewing them")
                    with open(file=content_dir + '/'  + filename, mode='w') as file:
                        file.write(file_contents)
                    return 'we ate a function, putting everything back'

        else:
            print("no comment found, inserting new comment")
            inserted = insert_comment_before_function(file_path=file_path, function_name=function_name, new_comment=new_comment_block)

            if checkfunctions:
                check_function_list = get_functions(filename=filename)
                if function_list == check_function_list:
                    if inserted:
                        return 'Inserted comment'
                    else:
                        return 'Function not found'
                else:
                    print("Something went horribly wrong, the functions in the file changed while reviewing them")
                    with open(file=content_dir + '/'  + filename, mode='w') as file:
                        file.write(file_contents)
                    return 'we ate a function, putting everything back'
    return 'Something went wrong with update_special_comment_block, you should never see this'


def remove_specialcomments_from_file(content, filename, function_name):

    pattern = r"'''([\s\S]*?:{}:{}\s-----Automated Review Start-----)(.*?)-----Automated Review End-----[\s\S]'''".format(re.escape(filename), re.escape(function_name))

    updated_content = re.sub(pattern=pattern, repl='', string=content, flags=re.DOTALL)

    return updated_content


def check_comment_hash(filename, function_name, hash):
    type = get_file_type(filename=filename)
    hash = hash_the_function(filename=filename, function_name=function_name )
    if type == 'python':
        contents = get_file_contents( filename=filename)
        pattern = hash + ":" + filename + ":" + function_name
        matches = re.findall(pattern=pattern, string=contents)
        if len(matches) > 0:
            return True
        else:
            return False
    else:
        return False


def find_hash_value(file_contents, filename, function_name):
    search_pattern = r"{}:{}[\s\S]-----Automated Review Start-----".format(re.escape(pattern=filename), re.escape(pattern=function_name))

    lines = file_contents.split('\n')

    for line in lines:
        match = re.search(pattern=search_pattern, string=line)
        if match:
            print("found match while looking for the hash")
            return line.split(':')[0]

    return None

def clean_up_mult_newlines(content):

    # Replace lines with only whitespace with a single newline
    content = re.sub(pattern=r'^[ \t]+$', repl='\n', string=content, flags=re.MULTILINE)

    # Replace consecutive newlines with just two newlines
    content = re.sub(pattern=r'\n{3,}', repl='\n\n', string=content)

    return content

#TODO: rewrite this to not be python specific
def insert_comment_before_function(file_path, function_name, new_comment):
    # Read the content of the file
    with open(file=file_path, mode='r') as file:
        lines = file.readlines()

    # Find the line number of the function's definition
    function_line = None
    for i, line in enumerate(iterable=lines):
        if f'def {function_name}(' in line:
            function_line = i
            break

    print (function_name + " is at line " + str(object=function_line))

    # If the function was found, insert the new comment before it
    if function_line is not None:
        lines.insert(function_line, new_comment + '\n')

        # Write the updated content back to the file
        with open(file=file_path, mode='w') as file:
            file.writelines(lines)

        return True  # Insertion successful
    else:
        return False  # Function not found
