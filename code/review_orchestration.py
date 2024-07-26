def review_doc(filename):
    function_status = {}
    file_contents = get_file_contents(CONTENT_DIR, filename)
    function_list = get_functions(filename, CONTENT_DIR, FILE_TYPES)
    orig_file_contents = file_contents

    #review the functions
    for function_name in function_list:
        print("Reviewing function: " + filename + ":" + function_name)
        function_status[function_name] = update_special_comment_block(function_name, filename, get_review_as_comment(filename, function_name), checkfunctions=True)
        print("Review complete: " + function_name + " status: " + function_status[function_name])

    #get the results to verify it all worked right
    after_file_contents = get_file_contents(CONTENT_DIR, filename)
    after_function_list = get_functions(filename, CONTENT_DIR, FILE_TYPES)


    #compare function_list and check_function_list
    if create_check_doc(file_contents, filename, function_list) == create_check_doc(after_file_contents,filename, function_list) and function_list == after_function_list:
        #fix any whitespace issues
        with open(CONTENT_DIR + '/'  + filename, 'w') as file:
            file.write(clean_up_mult_newlines(after_file_contents))
        print("All functions reviewed and new lines cleaned up")
        return function_status
    else:
        print("Something went horribly wrong, the functions in the file changed while reviewing them")
        #write file_contents back to the file
        with open(CONTENT_DIR + '/'  + filename, 'w') as file:
            file.write(orig_file_contents)

        with open(CONTENT_DIR + '/'  + filename + '.bad_doc_review', 'w') as file:
            file.write(create_check_doc(after_file_contents,filename, function_list))

        with open(CONTENT_DIR + '/'  + filename + '.pre_bad_doc_review', 'w') as file:
            file.write(create_check_doc(orig_file_contents,filename, function_list))
        
        return {}

def create_check_doc(content, filename, function_list):
    for function_name in function_list:
        content = remove_specialcomments_from_file(content, filename, function_name)
    content = clean_up_mult_newlines(content)
    return content