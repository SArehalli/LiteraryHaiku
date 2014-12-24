import requests
import random
import nltk
from nltk.corpus import cmudict
import re 
import itertools

HAIKU = (5, 7, 5)
HTML_HEADER = "html_header.html"
SYLL_DICT = cmudict.dict()

def generate_text(chain, syllables, current):
    
    # If theres only one choice, choose it
    if len(chain[current]) == 1:
        out = chain[current][0]

    # Otherwise, randomly pick a next word
    else:
        choice = random.randint(0, len(chain[current]) - 1)
        out = chain[current][choice]
    
    # Count syllables with nltk
    currentSyllables = 0
    if out in SYLL_DICT:
        # Use the CMU dict's syllable count if possible
        currentSyllables = len([x for x in SYLL_DICT[out][0] if re.match("\d",x[-1])])
    else:
        # Or use this BS syllable ocunt method.
        currentSyllables = len(re.findall(r"[aeiou]+", out))


    # If there are more syllables remaining
    if syllables - currentSyllables > 0:
        
        next_word = None 
        tries = 0
        
        # Try 5 times to get a next word that doesn't exceed the syllable count recursively
        while next_word is None and tries < 5:
            next_word = generate_text(chain, syllables - currentSyllables, out)
            tries += 1 
        
        # If that doesn't work, go back one step recursively and try that while loop.
        if next_word is None:
            return None

        # If everything did work, return and recurse back
        return out + " " +  next_word
    
    # If there are too many syllables, return None and recurse back. See previous code block for that mechanism
    if syllables - currentSyllables < 0:
        return None
    
    # If all is well, return
    else:
        return out

def haiku(text_file):
   # Open text data and remove commas
    with open(text_file) as f:
        text = re.findall(r"[\w']+", f.read())

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


