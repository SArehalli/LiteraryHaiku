import random
import requests
from flask import Flask
from flask import request
app = Flask(__name__)

def generate_text(chain, syllables, current):
    if len(chain[current]) == 1:
        out = chain[current][0]
    else:
        choice = random.randint(0, len(chain[current]) - 1)
        out = chain[current][choice]
    try:
        r = requests.post("http://rhymebrain.com/talk", {"function" : "getWordInfo",
                                                             "word" : out })
    except:
        print("Error: Could Not connect to RhymeBrain API")
        return None
    if syllables - int(r.json()['syllables']) > 0:
        next_word = None 
        tries = 0
        while next_word is None and tries < 5:
            next_word = generate_text(chain, syllables - int(r.json()['syllables']), out)
            tries += 1 
        if next_word is None:
            return None
        return out + " " + next_word
             
    if syllables - int(r.json()['syllables']) < 0:
        return None
    else:
        return out

@app.route("/haiku", methods=['POST', 'GET'])
def haiku():
    if request.method == 'POST':
        try:
            text = request.form['text']
        except:
            text = "cask.txt"
    # Open text data and remove commas
    with open("./text.txt") as f:
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
    output = ""
    for line in poem[1:]:
        output.append(line.capitalize() + "<br>")
    return output

