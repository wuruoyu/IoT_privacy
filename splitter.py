from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
import itertools
from collections import Counter
import re
import json

# word dict
WORDS = words.words()
WORDS.append('id')
WORDS.append('max')
WORDS.append('min')
WORDS.append('config')
WORDS.append('app')
WORDS.append('url')

COUNTS = Counter(WORDS)
lemmatizer = WordNetLemmatizer()

def has_space(text):
    return any(word.find(' ') != -1 for word in text)

def has_hyphen(text):
    return any(word.find('-') != -1 for word in text)

def has_underscore(text):
    return any(word.find('_') != -1 for word in text)

def has_digit(word):
    return any(char.isdigit() for char in word)

def has_both_case(word):
    return (any(char.islower() for char in word[1:]) and any(not char.islower() for char in word[1:]))

def handle_camel_case(word):
    return re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', word)).split()

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
    candidates = ([lemmatizer.lemmatize(first)] + segment(rest) for (first, rest) in splits(text, 1))
    return max(candidates, key=Pwords)

def split(text):
    print(text)
    lower_words = []
    ret_words = []

    # split 
    if has_space(text):
        # text = text.split()
        text = list(itertools.chain(*[word.split() for word in text]))
    if has_hyphen(text):
        text = list(itertools.chain(*[word.split('-') for word in text]))
    if has_underscore(text):
        text = list(itertools.chain(*[word.split('_') for word in text]))

    # handle camel case
    for word in text:
        if has_both_case(word):
            lower_words = lower_words + handle_camel_case(word)
        else:
            lower_words.append(word)

    # lower the case
    for idx in range(len(lower_words)):
        lower_words[idx] = lower_words[idx].lower()

    # normal case
    for word in lower_words:
        # dont handle digit
        if has_digit(word):
            ret_words.append(word)
        # too short
        if len(word) <= 3:
            ret_words.append(word)
        else:
            ret_words = ret_words + segment(word)

    print(ret_words)

    print("----------")
    return ret_words


split(['open Lights Bulb with id'])
split(['openLightsBulbWithId'])
split(['open-Lights-Bulb-With-Id'])
split(['open Lights-Bulb With ID'])
split(['open_lights_bulk_with_id'])
split(['open lights_bulk with id'])
split(['openlightsbulbwithid'])
split(['modelid'])
split(['bri'])
split(['config'])
