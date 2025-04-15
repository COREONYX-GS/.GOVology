import os
import random
import json
import pandas as pd
import numpy as np
import math

from nltk.corpus import words
from nltk.corpus import wordnet as wn

from openai import OpenAI
client = OpenAI()

word_list = [w for w in set(words.words()) if len(w) > 3]

###############################################################################################
# https://stackoverflow.com/questions/58044209/how-to-find-if-a-word-is-in-a-string-fast-python
class AhoNode:
    def __init__(self):
        self.goto = {}
        self.out = []
        self.fail = None

def aho_create_forest(patterns):
    root = AhoNode()

    for path in patterns:
        node = root
        for symbol in path:
            node = node.goto.setdefault(symbol, AhoNode())
        node.out.append(path)
    return root

def aho_create_statemachine(patterns):
    root = aho_create_forest(patterns)
    queue = []
    for node in root.goto.values():
        queue.append(node)
        node.fail = root

    while len(queue) > 0:
        rnode = queue.pop(0)

        for key, unode in rnode.goto.items():
            queue.append(unode)
            fnode = rnode.fail
            while fnode != None and not key in fnode.goto:
                fnode = fnode.fail
            unode.fail = fnode.goto[key] if fnode else root
            unode.out += unode.fail.out

    return root

def aho_find_all(s, root, callback):
    node = root
    words_found = {}

    for i in range(len(s)):
        while node != None and not s[i] in node.goto:
            node = node.fail
        if node == None:
            node = root
            continue
        node = node.goto[s[i]]
        for pattern in node.out:
            if callback:
                callback(i - len(pattern) + 1, pattern)
            else:
                words_found[pattern] = i - len(pattern) + 1
    
    return words_found

aho_root = aho_create_statemachine(word_list)
###############################################################################################

def domain_is_agency(name):
    syns = wn.synsets(name)
    for w in syns:
        if "agency" in w.definition():
            return True

    return False

def domain_is_words(name):
    return aho_find_all(name, aho_root, None)

def domain_is_noun(name):
    def is_noun(name):
        #return any('n' in synset.lexname() for synset in wn.synsets(word))
        return any(synset.lexname().startswith('noun') for synset in wn.synsets(name))

    words = name.split('.')
    return any(is_noun(word) for word in words)

def domain_is_verb(name):
    def is_verb(name):
        #return any('v' in synset.lexname() for synset in wn.synsets(word))
        return any(synset.lexname().startswith('verb') for synset in wn.synsets(name))

    words = name.split('.')
    return any(is_verb(word) for word in words)

def domain_is_acronym(name):
    syns = wn.synsets(name)

    for w in syns:
        if "agency" in w.definition():
            return True

        if name == w.name().split('.')[0]:
            return False
    
    if domain_is_noun(name) or domain_is_verb(name):
        return False

    if domain_is_words(name):
        return False

    return True


def grid_dimensions(count, aspect_ratio=(16, 9), buffer=1.0):
    """
    Calculate grid dimensions (max_x, max_y) for a given number of items.

    Args:
        count (int): Total number of items.
        aspect_ratio (tuple): Desired aspect ratio as (width, height).
        buffer (float): Buffer factor to increase the count (default is 1.0 for no extra buffer).

    Returns:
        tuple: (max_x, max_y) dimensions of the grid.
    """
    # Adjust count for buffer if needed
    adjusted_count = count * buffer
    # Calculate the ratio as width/height (e.g., 16/9)
    ratio = aspect_ratio[0] / aspect_ratio[1]
    
    # Calculate grid dimensions using the derived formula
    max_x = math.ceil(math.sqrt(adjusted_count * ratio))
    max_y = math.ceil(math.sqrt(adjusted_count / ratio))
    
    return max_x, max_y

def generate_data(FILE_IN):
    data = []
    df = pd.read_csv(FILE_IN)
    count, _ = df.shape
    max_x, max_y = grid_dimensions(count, aspect_ratio=(16, 9), buffer=1.2)
    cur_x, cur_y = 0, 0

    df = df.sort_values(by="Agency")
    for _, row in df.iterrows():
        name = row.get("Domain name", "").strip().replace(".gov", "").lower()
        if name:  # Generate random coordinates in some bounding range
            x = cur_x
            y = cur_y
                
            # You can store any additional fields you like;
            # for now, we'll just keep domain, x, y
            data.append({
                "domain": name,
                "agency": row.get("Agency", "").strip(),
                "org": row.get("Organization name", "").strip(),
                "x": x,
                "y": y,
                "length": len(name),
                "is_agency": domain_is_agency(name), 
                "is_words": domain_is_words(name), 
                "is_acronym": domain_is_acronym(name), 
                "is_noun": domain_is_noun(name), 
                "is_verb": domain_is_verb(name), 
            })

            print(f"{name} -> x: {x}, y: {y} (max_x: {max_x}, max_y: {max_y})")

            cur_y += 1
            if cur_y >= max_y:
                cur_y = 0
                cur_x += 1

            if cur_x > max_x:
                print("Warning: Exceeded grid dimensions!")
        else:
            print(f"Warning: Empty domain name found: {row.get("Domain name")}")
            print(_)
            print(row)


    return data

def load_old_data(FILENAME):
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def get_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def merge_data(new, old):
    old_map = {item['domain']: item for item in old}
    for item in new:
        if item['domain'] in old_map:
            item['embedding'] = old_map[item['domain']].get('embedding', None)

        if not item['embedding']:
            item['embedding'] = get_embedding(item['domain'])
    
    return new_data

def save_data(data, json_filename = "gov-elements.json"):
    with open(json_filename, 'w', encoding='utf-8') as out:
        json.dump(data, out, indent=4)
    
if __name__ == "__main__":
    DATA_FILE_IN = os.getenv("DATA_FILE_IN", "data/federal-domains.csv")
    DATA_FILE_OUT = os.getenv("DATA_FILE_OUT", "data/gov-elements.json")

    # old_data = load_old_data(DATA_FILE_OUT)
    # new_data = generate_data(DATA_FILE_IN)
    data = generate_data(DATA_FILE_IN)
    # data = merge_data(new_data, old_data)

    save_data(data, DATA_FILE_OUT)

    print(f"Data saved with {len(data)} entries.")


