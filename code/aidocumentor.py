import os
import sys

#my modules
from config_manager import get_config, read_file_types
from file_operations import list_files, get_file_contents
from function_analyzer import get_functions, get_function_by_name, get_file_contents  
from comment_manager import get_review_as_comment, read_special_comment_block, update_special_comment_block, remove_specialcomments_from_file
from review_orchestration import review_doc, create_check_doc

#globals
PROMPT_BEGIN = os.environ.get('PROMPT_BEGIN', default='Riddle me this Batman: ')
CONFIG_FILE = "~/.ssh/aidocumentor_config.json"
CONTENT_DIR = "/app/data"

def help():
    print("This AI tool can look at the current directory and answer questions or do updates")
    print("Commands are: ")
    print("     help - prints this help message")
    print("     list - lists the files in the current directory")
    print("     review_doc <filename> - reviews all the functions in the file and updates the special comment blocks")
    print("     review_docs - reviews all the functions in all the files in the current directory and updates the special comment blocks")

def main():
    get_config(config_file=CONFIG_FILE, content_dir=CONTENT_DIR)

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
            functions = get_functions(filename=filename)
            print(functions)
        elif command == 'function':
            filename = sys.argv[2]
            function_name = sys.argv[3]
            function = get_function_by_name(filename=filename, function_name=function_name)
            #print the formatted function results
            print("Function: " + function_name)
            print("Args: " + function['args'])
            print("Lines: " + function['lines'])
        elif command == 'review_function':
            filename = sys.argv[2]
            function_name = sys.argv[3]
            review = get_review_as_comment(filename=filename, function_name=function_name)
            print(review)
        elif command == 'get_comments':
            filename = sys.argv[2]
            function_name = sys.argv[3]
            comment_dict = read_special_comment_block(function_name=function_name, filename=filename)
            if comment_dict:
                for key, value in comment_dict.items():
                    print(f"{key}: {value}")
            else:
                print("Special comment block not found.")
        elif command == 'update_comments':
            filename = sys.argv[2]
            function_name = sys.argv[3]
            print(update_special_comment_block(function_name=function_name, filename=filename, new_comment_block=get_review_as_comment(filename=filename, function_name=function_name)))
        elif command == 'remove_review':
            filename = sys.argv[2]
            function_name = sys.argv[3]
            print(update_special_comment_block(function_name=function_name, filename=filename, new_comment_block=' ', checkfunctions=False))

            print("Review removed")
        elif command == 'review_doc':
            filename = sys.argv[2]
            print(review_doc(filename=filename))
        elif command == 'check_doc':
            filename = sys.argv[2]
            function_list = get_functions(filename=filename)
            file_contents = get_file_contents(filename=filename)
            with open(file=CONTENT_DIR + '/'  + filename + '.check_doc', mode='w') as file:
                file.write(create_check_doc(content=file_contents, filename=filename, function_list=function_list))
            print ("check doc created as " + filename + ".check_doc")
        elif command == 'review_docs':
            files = list_files()
            for filename in files:
                file_types = read_file_types()
                if filename.endswith(tuple(iterable=file_types['python']['extensions'])):
                    print("Reviewing file: " + filename)
                    review_doc(filename=filename)
            print("Review complete")
        else:
            print("Unknown command: " + command)
            help()
            exit()



if __name__ == '__main__':
    main()