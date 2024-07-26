import json
import openai


from config_manager import get_api_key, read_file_types
from function_analyzer import get_function_by_name, get_functions, get_file_type
from utils import array_to_string, parse_file



def send_prompt(prompt):
    #abstraction to allow other ai engines to be used later, I'd really like to switch to claud here
    return send_prompt_openai(prompt=prompt)

def send_prompt_openai(prompt):
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

    #set the key from the config if it is not already set
    if "api_key" not in openai or openai.api_key == '' or openai.api_key == None:
        openai.api_key = get_api_key()


    model="gpt-4o-mini"
    messages=[
        {"role": "system", "content": "You are a senior software engineer."},
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
    myresponse = json.loads(s=json.dumps(obj=myresponse))
    del myresponse['choices']
    myresponse = json.dumps(obj=myresponse)
    #print (myresponse)
    #print (mycontent)

    return response



def review_function(filename, function_name):
    #get the function
    function = get_function_by_name(filename=filename, function_name=function_name)
    file_types = read_file_types()
    type_details = file_types[get_file_type(filename=filename)]

    #TODO: add expertise from the file contents too
    role_array = type_details['role']
    expertise_array = type_details['expertise']

    #create keyvalue pair of vars to pass to the file parser
    my_vars = {
        'role': array_to_string(array=role_array),
        'expertise': array_to_string(array=expertise_array),
        'function_name': function_name,
        'filetype': get_file_type(filename=filename),
        'file_functions': array_to_string(array=get_functions(filename=filename)),
        'args': function['args'],
        'lines': function['lines']
    }

    #get the prompt
    prompt = parse_file(filename='functionprompt.txt', vars=my_vars)

    #send the prompt
    return  send_prompt(prompt=prompt)


def fetch_review(filename, function_name, max_retries=10):
    for _ in range(max_retries):
        review = review_function(filename=filename, function_name=function_name)  # Replace with your actual code to fetch the review
        
        try:
            #review_str = str(review)
            review_str = str(object=review['choices'][0]['message']['content'])
            review_json = json.loads(review_str )
            return review_json  # Return the JSON object if parsing is successful
        except json.JSONDecodeError:
            # Parsing failed, retry
            continue
    
    return None  # Return None if all retries failed
    