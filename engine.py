import spacy
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import ssl
import re
from terms import IGNORE, STOP, SAVE_WORDS, SAVE_PHRASES, format_term
from config import config as CONFIG

# workaround to get nltk to work...
# https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# ================================================================================
#
# Spacy engine
#
# ================================================================================

model = "en_core_web_md"

nlp = spacy.load(model)

def get_ents(doc, debug = False):
    output = []
    ignore = ["CARDINAL", "DATE"]

    # show the category of each entity
    if debug:
        for ent in doc.ents:
            print(ent, ent.label_)

    # remove unwanted categories
    for ent in doc.ents:
        if ent.label_ in ignore:
            continue
        output.append(str(ent))

    return output

def engine_spacify(text):
    doc = nlp(text)
    # get the entities from spacy
    ents = get_ents(doc, False)
    word_list = []

    replaceChars = ["&","/","and"]

    for ent in ents:
        for char in replaceChars:
            if char in ent:
                ent = ent.replace(char, ",")
        if "," in ent:
            for word in ent.split(","):
                word_list.append(word.strip())
        else:
            word_list.append(ent)
    
    save_terms = find_save_terms(doc)
    word_list = word_list + save_terms
    
    output = normalize_results(word_list)
    return set(output)

def find_save_terms(doc):
    if doc == None:
        print("find_save_terms: no doc?")
        return []
    
    output = []
    for token in doc:
        if token.text in SAVE_WORDS:
            output.append(token.text)
    
    text = doc.text.lower()
    for phrase in SAVE_PHRASES:
        if phrase in text:
            output.append(phrase)
    
    return output


# =====================================================================
#
# NLTK engine
#
# =====================================================================

nltk.download('punkt', quiet=(not CONFIG.debug_mode))
nltk.download('wordnet', quiet=(not CONFIG.debug_mode))
nltk.download('stopwords', quiet=(not CONFIG.debug_mode))
nltk.download('averaged_perceptron_tagger', quiet=(not CONFIG.debug_mode))

nltk_stop = set(stopwords.words('english'))
STOP_WORDS = nltk_stop.union(STOP)

lemmatizer = WordNetLemmatizer()


def engine_nltk(s, debug = False):
    if debug:
        print(s)

    # find any existing save words - words we want to intercept and save regardless of what NLTK thinks
    exclude = {',', ':', ';', '!', '(', ')', '[', ']'} # cut out these punc
    temp = ''.join(ch for ch in s if ch not in exclude).lower()
    #temp = s.lower()
    # find phrases in the string that might include spaces (or slashes, like 'pl/sql')
    # note: this may add performance slowdown since we are doing more iteration and checking for substrings here
    skip = set()
    savePhrases = []
    for phrase in SAVE_PHRASES:
        if phrase in temp:
            skip = skip.union(set(phrase.split())) # don't count this word individually since its part of a phrase
            savePhrases.append(phrase)

    temp = ', or '.join(temp.split('/')) # replace / with ', or ' so they are seen as separate terms and understood by NLTK
    saveWords = [word for word in temp.split() if word in SAVE_WORDS]

    ignore = skip.union(IGNORE)

    s = ', or '.join(s.split('/')) # replace / with ', or ' so they are seen as separate terms and understood by NLTK

    # NLTK tries to find nouns
    tagged = pos_tag(s)
    nouns = [lemmatize(word) for (word, pos) in tagged if 'NN' in pos]

    # combine our saveWords and NLTK's nouns
    # remove stop words or ignore words
    allTheWords = nouns + saveWords + savePhrases
    word_list = []
    for word in allTheWords:
        if (word in ignore):
            continue
        if (word in STOP_WORDS):
            continue
        word_list.append(word)
    
    output = normalize_results(word_list)
    output = set(output)
    return output

def pos_tag(s):
    'add part-of-speech tags to words in a sentence'
    tokenized = nltk.word_tokenize(s)
    tagged = [(word, pos) for (word, pos) in nltk.pos_tag(tokenized)]
    return tagged

def lemmatize(word):
    'convert word into singular form'
    # prevent non-words ending with 's' from being lemmatized incorrectly
    if len(word) <= 3:
        return word
    return lemmatizer.lemmatize(word)

def getFreqDist(keywords_list, enforce_minimum = True):
    freq_keywords = nltk.FreqDist(keywords_list)
    freq_keywords = [(word, freq) for (word, freq) in freq_keywords.most_common() if (not enforce_minimum) or (freq >= CONFIG.keyword_freq)]
    return freq_keywords


# =====================================================================
#
# General - Utils
#
# =====================================================================

def normalize_results(word_list):
    output = []
    for word in word_list:
        output.append(format_term(word))
    return output