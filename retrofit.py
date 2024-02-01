from googlecloud import download, upload_json
from terms import IGNORE, CONFLATE, format_term
from json import dump
from config import config

URL = 'https://storage.googleapis.com/storage/v1/b/{}/o'

def applyIgnore(data):
    output = []
    for (name, json) in data:
        change = False
        newJson = []
        erase = []
        studyCount = json[0]
        newJson.append(studyCount)
        for i in range(1, len(json)):
            if json[i][0] in IGNORE:
                erase.append(json[i][0])
                change = True
                continue
            # cut terms that are too infrequent, since we never will show them
            if json[i][1] / studyCount < config.freq_threshold:
                erase.append(json[i][0])
                change = True
                continue
            newJson.append(json[i])
        if change:
            print(f'{name}.json: erased {len(erase)} terms')
            print(erase)
            output.append((name, newJson))
    if len(output) == 0:
        print(f'no changes made; everything is up to date!')
        return data
    if input('save these changes? (y/n): ').lower() == 'y':
        return output
    return data

def applyConflate(data):
    output = []
    for (name, json) in data:
        change = False
        newJson = []
        confl = []
        wordsUpdated = 0
        newJson.append(json[0]) # study count
        for i in range(1, len(json)):
            word = json[i][0]
            # see if word needs to be conflated to a preferred form
            if word.lower() in CONFLATE:
                conflated = CONFLATE[word.lower()]
                if word != conflated:
                    confl.append((word, conflated))
                    newJson.append((conflated, json[i][1]))
                    change = True
                    continue
            # see if word should be formatted differently
            else:
                newFormat = format_term(word)
                if word != newFormat:
                    newJson.append((newFormat, json[i][1]))
                    change = True
                    wordsUpdated += 1
                    continue
            newJson.append(json[i])
        if change:
            print(f'{name}.json: conflated {len(confl)} terms')
            for (before, after) in confl:
                print(f'{before} -> {after}')
            print(f'Number of terms reformatted: {wordsUpdated}')
            
            # combine all identical terms, since there may be multiple forms of the same term that were conflated
            studyCount = newJson[0]
            tuples = newJson[1:]
            # sort alphabetically
            tuples = sorted(tuples, key = lambda x: x[0])
            newTuples = []
            for (word, count) in tuples:
                if len(newTuples) == 0:
                    newTuples.append((word, count))
                    continue
                currentComp = newTuples[-1]
                if currentComp[0] == word:
                    print(f'combining! word = {word}')
                    newTuples[-1] = (currentComp[0], currentComp[1] + count)
                else: 
                    newTuples.append((word, count))
            # sort by frequency
            newTuples = sorted(newTuples, key = lambda x: x[1], reverse = True)
            newJson = [studyCount] + newTuples
            output.append((name, newJson))
    if len(output) == 0:
        print(f'no changes made; everything is up to date!')
        return data
    if input('save these changes? (y/n): ').lower() == 'y':
        return output
    return data

def uploadRevisions(data):
    for (name, json) in data:
        filename = f'{name}_retrofit'
        writeToJSON(json, filename)
        upload_json(filename)


def writeToJSON(data, filename):
    'writes the keywords data to a local json file. file will be saved in a ./data/ directory.'

    with open('data/{}.json'.format(filename), 'w', encoding='utf-8') as f:
        dump(data, f, ensure_ascii=False, indent=4)

data = download()
data = applyIgnore(data)
data = applyConflate(data)

for (name, json) in data:
    print('======================')
    print(f'reviewing {name}.json')
    print(json)
    input('== Enter to continue ==')

uploadRevisions(data)