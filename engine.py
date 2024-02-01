import spacy
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import ssl
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
    '''
    Uses Spacy to find keywords in a given string.

    Breaks a given string down to its entities, and returns entities of specific categories.
    '''
    doc = nlp(text)

    # get the entities from spacy
    ents = get_ents(doc, False)
    word_list = []

    replaceChars = ["&","/","and"]

    for ent in ents:
        for char in replaceChars:
            if char in ent:
                ent = ent.replace(char, " ")
        if "," in ent:
            ent = ent.replace(",", " ")
        for word in ent.split():
            word_list.append(word.strip())
    return word_list


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
    '''
    Uses NLTK to find keywords in the given string.

    As of now, it's pretty unsophisiticated - it just gets the nouns.
    (well, it tries its best, but often non-nouns slip through lol)
    '''
    if debug:
        print(s)
    
    # replace / with ', or ' so they are seen as separate terms and understood better by NLTK
    s = ', or '.join(s.split('/')) 

    # tag the 'part of speech' for each word and get the nouns from the string
    tagged = pos_tag(s)
    nouns = [word for (word, pos) in tagged if 'NN' in pos]
    
    return nouns

def pos_tag(s):
    'add part-of-speech tags to words in a sentence'
    tokenized = nltk.word_tokenize(s)
    tagged = [(word, pos) for (word, pos) in nltk.pos_tag(tokenized)]
    return tagged

def lemmatize(word: str):
    'convert word into singular form'
    # prevent non-words ending with 's' from being lemmatized incorrectly
    if len(word) <= 3:
        return word
    # make word lowercase - seems to help a lot for some reason
    cap = word.istitle()
    temp = word.lower()

    # attempt lemmatization - if nothing changes, try lemmatizing as other parts of speech
    out = lemmatizer.lemmatize(temp)
    if out == temp:
        out = lemmatizer.lemmatize(temp, "v")
    if out == temp:
        out = lemmatizer.lemmatize(temp, "a")

    if cap:
        out = out.capitalize()
    return out

def getFreqDist(keywords_list, enforce_minimum = True):
    'uses NLTK to calculate a frequency distribution for the words in a list'
    freq_keywords = nltk.FreqDist(keywords_list)
    freq_keywords = [(word, freq) for (word, freq) in freq_keywords.most_common() if (not enforce_minimum) or (freq >= CONFIG.keyword_freq)]
    return freq_keywords


# =====================================================================
#
# General - Utils
#
# =====================================================================

def run_engine(mode, s):
    'runs the selected engines against the input string to extract a set of keywords and terms'
    word_list_nltk = []
    word_list_spacy = []

    # find the save terms from this string
    saveTerms, skip = find_save_terms(s)

    # use an NLP engine to find keywords and terms
    if mode == 1 or mode == 3:
        word_list_nltk = engine_nltk(s)
    if mode == 2 or mode == 3:
        word_list_spacy = engine_spacify(s)
    
    # remove the ignore terms
    word_list = word_list_nltk + word_list_spacy
    word_list = filter_bad_terms(word_list, skip)

    # join it all together and normalize the results
    word_list = word_list + saveTerms
    output = normalize_results(word_list)
    return output

def normalize_results(word_list):
    'put terms in their standardized/preferred format, and remove any duplicates'
    output = set()
    for word in word_list:
        output.add(format_term(word))
    return output

def find_save_terms(s):
     # remove punctuation that might interfere and make lowercase
    exclude = {',', ':', ';', '!', '(', ')', '[', ']'}
    temp = ''.join(ch for ch in s if ch not in exclude).lower()

    # find phrases in the string that might include spaces (or slashes, like 'pl/sql')
    skip = set() # keep track of the pieces of phrases that we add, so they aren't re-added a second time
    savePhrases = []
    for phrase in SAVE_PHRASES:
        if phrase in temp:
            skip = skip.union(set(phrase.split())) # don't count this word individually since its part of a phrase
            savePhrases.append(phrase)

    # find individual save words
    temp = temp.replace("/", " ") # replace slashes with spaces so it'll split those terms too
    saveWords = [word for word in temp.split() if word in SAVE_WORDS]

    return saveWords + savePhrases, skip

def filter_bad_terms(words: list[str], skip: set[str]):
    ignore = IGNORE.union(skip, STOP_WORDS)
    output = []

    for word in words:
        word = word.lower()
        if (word in ignore) or (lemmatize(word) in ignore):
            continue
        output.append(word)
    
    return output

def test_lemmatize():
    tests = [
        ("Engineers", "Engineer"),
        ("engineers", "engineer"),
        ("Requirements", "Requirement"),
        ("requirements", "requirement"),
        ("Responsibilities", "Responsibility"),
        ("responsibilities", "responsibility"),
        ("provides", "provide"),
        ("relies", "rely"),
        ("Improves", "Improve"),
    ]
    score = 0
    outOf = 0
    for case in tests:
        out = lemmatize(case[0])
        expOut = case[1]
        if (out == expOut):
            score += 1
        else:
            print("failed case:")
            print("{} => {} (exp. {})".format(case[0], out, expOut))
        outOf += 1
    
    print("Accuracy: {}%".format(round(score / outOf * 100)))

#test_lemmatize()