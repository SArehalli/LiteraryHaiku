import requests
import random

HAIKU = (5, 7, 5)
HTML_HEADER = "../html_header.html"

def generate_text(chain, syllables, current):
    
    # If theres only one choice, choose it
    if len(chain[current]) == 1:
        out = chain[current][0]

    # Otherwise, randomly pick a next word
    else:
        choice = random.randint(0, len(chain[current]) - 1)
        out = chain[current][choice]
    
    # Get the syllable count of the chosen word (out) through Rhymebrain. NOTE: Find a better way to do this. NLTK? 
    try:
        r = requests.post("http://rhymebrain.com/talk", {"function" : "getWordInfo",
                                                             "word" : out })
    # Or exit because you can't connect
    except:
        return "Error: Could Not connect to RhymeBrain API"
    
    # If there are more syllables remaining
    if syllables - int(r.json()['syllables']) > 0:
        
        next_word = None 
        tries = 0
        
        # Try 5 times to get a next word that doesn't exceed the syllable count recursively
        while next_word is None and tries < 5:
            next_word = generate_text(chain, syllables - int(r.json()['syllables']), out)
            tries += 1 
        
        # If that doesn't work, go back one step recursively and try that while loop.
        if next_word is None:
            return None

        # If everything did work, return and recurse back
        return out + " " + next_word
    
    # If there are too many syllables, return None and recurse back. See previous code block for that mechanism
    if syllables - int(r.json()['syllables']) < 0:
        return None
    
    # If all is well, return
    else:
        return out

def haiku(text_file):
   # Open text data and remove commas
    with open(text_file) as f:
        text = f.read().split()
        text = [a.strip("\"") for a in text]
        for word in text:
            if word[-1] in ( ",", "\""):
                word = word[:-1]

    # Create the Markov Chain
    chain = {}
    for i in range(0, len(text)-1):
        if text[i] in chain:
            chain[text[i]].append(text[i+1])
        else:
            chain[text[i]] = [text[i+1]]
    
    # Choose generator word. This is not printed 
    poem = [text[random.randint(0, len(text))]]

    # Write the Haiku using generate_text() 
    for syl in HAIKU:
        line = None
        while line is None:
            line = generate_text(chain, syl, poem[-1].split()[-1])
        poem.append(line)
    
    # Print the Completed Haiku
    html = open(HTML_HEADER)
    output = html.read() + "<div class='haiku'>"
    for line in poem[1:]:
        output += line.capitalize() + "<br>"
    return output + "</div></div></body></html>"


