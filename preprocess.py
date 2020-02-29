import json
from nltk.corpus import words
from nltk.corpus import stopwords
from collections import Counter
import re
from nltk.stem import WordNetLemmatizer
from IPython import embed

lemmatizer = WordNetLemmatizer()

with open('./training-data-for-classifier/(iot)-hue_jsons.txt') as json_file:
    data = json.load(json_file)

WORDS = words.words()
STOPWORDS = list(set(stopwords.words('english')))
COUNTS = Counter(WORDS)

def pdist(counter):
    N = sum(counter.values())
    return lambda x: counter[x]/N

P = pdist(COUNTS)

def Pwords(words):
    return product(P(w) for w in words)

def product(nums):
    result = 1
    for x in nums:
        result *= x
    return result

def splits(text, start=0, L=20):
    return [(text[:i], text[i:]) for i in range(start, min(len(text), L)+1)]

def segment(text):
    if not text:
        return []
    else:
        candidates = ([lemmatizer.lemmatize(first)] + segment(rest) for (first, rest) in splits(text, 1))
        return max(candidates, key=Pwords)

def hasNumber(string):
    return any(char.isdigit() for char in string)

def hasSpace(string):
    for char in string:
        if char == ' ':
            return True
    return False

def str_process(string):
    # case
    string = string.lower()

    # no digit
    if hasNumber(string) or hasSpace(string):
        return string

    # segment
    ret_str = ""
    for word in segment(string):
        ret_str = ret_str + word
        ret_str = ret_str + " "
    return ret_str 

def iterate_json(data):
    if type(data) == list:
        new_list = []
        for item in data:
            if type(item) == list or type(item) == dict:
                new_list.append(iterate_json(item))
            elif type(item) == str:
                new_list.append(str_process(item))
            else:
                new_list.append(item)
        return new_list
    elif type(data) == dict:
        new_dict = {}
        for key, values in data.items():
            if type(key) == str:
                new_key = str_process(key)
            else:
                new_key = key
            if type(values) == list or type(values) == dict:
                new_dict[new_key] = iterate_json(values)
            elif type(values) == str:
                new_dict[new_key] = str_process(values)
            else:
                new_dict[new_key] = values
        return new_dict

new_data = iterate_json(data)
print(len(new_data))

embed()

with open('preprocess.txt', 'w') as outfile:
    json.dump(new_data, outfile)
