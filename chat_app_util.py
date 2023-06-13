# file with some helper functions
import dash
from dash import html

# contant for now, unless we want to import a library to dynamically get screen size...
CONST_LENGTH = 60

# split a long string into smaller chunks
def split_text(text):
    chunked = [""]
    if len(text) < CONST_LENGTH:
        return [text]

    # IMPORTANT: at the moment this assumes the input will have spaces, not just one long string
    sections = text.split(" ")

    current_line = 0
    for s in sections:
        if (len(chunked[current_line]) + len(s)) >= CONST_LENGTH:
            current_line += 1
            chunked.append(s)
        else:
            chunked[current_line] = chunked[current_line] + " " + s

    chunked.reverse()  # order reversed due to use of CSS to keep new text on the screen when generated
    return chunked

# given a JSON response, format it ina  way that will be nice to display
def format_responses(response):
    formatted_res = []
    for r in response:
        print(r)
        res_number = [
            html.P("Response # " + str(r["ranking"]), 
                   style={'text-align': 'left', "margin" : "1px"})
        ]
        
        res_message = split_text(r["message"])
        res_message = [
            html.P(html.I(res),
                   style={'text-align': 'left', "margin" : "1px"})
                   for res in res_message
        ]

        dataset_url = [
            html.P(html.A(r["dataset_url"], href=r["dataset_url"]),
                   style={'text-align': 'left', "margin" : "1px"})
            ]

        formatted_res = dataset_url + res_message + res_number + formatted_res
    
    return formatted_res
