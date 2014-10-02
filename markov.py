import random
import requests

# Open text data and remove commas
with open("./text.txt") as f:
    text = f.read().split()
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


# Generate Output
def generate_text(chain, syllables, current):
    if len(chain[current]) == 1:
        out = chain[current][0]
    else:
        choice = random.randint(0, len(chain[current]) - 1)
        out = chain[current][choice]
    r = requests.post("http://rhymebrain.com/talk", {"function" : "getWordInfo",
                                                         "word" : out })
    if syllables - int(r.json()['syllables']) > 0:
        return out + " " +  generate_text(chain, syllables - int(r.json()['syllables']), out) 
    else:
        return out
line = []
line.append(generate_text(chain, 5, "I"))
line.append(generate_text(chain, 7, line[-1].split()[-1]))
line.append(generate_text(chain, 5, line[-1].split()[-1]))
for thing in line:
    print(thing)
