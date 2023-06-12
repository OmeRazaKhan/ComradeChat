# file with some helper functions

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