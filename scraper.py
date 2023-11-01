from bs4 import BeautifulSoup, element
import requests
import time
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import ssl
import time
from socket import error
import json
from datetime import datetime
from config import config as CONFIG, debugger as DEBUG

# to use your own dataset, change this import to point to your own version of terms.py
from terms import IGNORE, STOP, SAVE_WORDS, SAVE_PHRASES, CONFLATE


# workaround to get nltk to work...
# https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=(not CONFIG.debug_mode))
nltk.download('wordnet', quiet=(not CONFIG.debug_mode))
nltk.download('stopwords', quiet=(not CONFIG.debug_mode))
nltk.download('averaged_perceptron_tagger', quiet=(not CONFIG.debug_mode))

lemmatizer = WordNetLemmatizer()

nltk_stop = set(stopwords.words('english'))
STOP_WORDS = nltk_stop.union(STOP)


class classNames:
    title = 'topcard__title'

    # body of the job description, including requirements and nice-to-haves
    # strong tags indicate headers
    # - might be useful to identify required skills vs nice-to-haves?
    description = 'description__text'

    # criteria list:
    # first: seniority
    # second: employment type (fulltime, contract, etc)
    criteria = 'description__job-criteria-item'

SEARCH_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={0}'
JOB_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'

def pause(sec, force = False):
    'time.sleep that abides by config rules'
    if CONFIG.enable_pausing or force:
        time.sleep(sec)

def consoleLog(s):
    'logging to console (print) that abides by config rules'
    if CONFIG.enable_misc_logging:
        print(s)

def getSearchURL(keyword, start = 0, location = None):
    'returns a URL for the job ID search HTTP request'
    url = SEARCH_URL.format(keyword)

    if (location != None):
        url = url + '&location={}'.format(location)
    
    url = url + '&start={}'.format(start)
    return url

def scrapeLinkedIn(test_IDs = None, saveOutput = True):
    '''
    Entry point for running the linked-in web scraper.
    Returns a frequency distribution of format: [(word, freq), (word2, freq), ...].

    test_IDs: list of job IDs to use for testing - skips the getJobIDs step.
    saveOutput: boolean to toggle if output should be saved to a json. json is saved to ./data/ directory.
    '''
    # display config
    if (CONFIG.debug_mode):
        print('DEBUG MODE: on')
        if (DEBUG.find_terms):
            print('FIND TERMS: on')
        pause(3)

    if test_IDs != None:
        print('{} test IDs provided! skipping jobID search.'.format(len(test_IDs)))
        jobIDs = test_IDs
    else:
        jobIDs = getJobIDs()
    
    (keywords_list, skipped_jobs) = mainWorkflow(jobIDs)

    # if there were any skipped jobs, try re-doing them
    if (len(skipped_jobs) > 0):
        retry = CONFIG.retry_count
        pause(2)

        consoleLog('Attempting to resolve skipped jobs. Will attempt up to {} times.'.format(retry))
        no_change = 0

        for i in range(retry):
            if (len(skipped_jobs) == 0):
                consoleLog('all jobs searched!')
                break
            if (i > 0):
                consoleLog('restart!')
            consoleLog('iteration {}/{}'.format(i+1, retry))
            pause(0.5)
            last_skipped_count = len(skipped_jobs)
            (skip_keywords, skipped_jobs) = mainWorkflow(skipped_jobs)
            if (last_skipped_count == len(skipped_jobs)):
                no_change += 1
                if (no_change >= 2):
                    consoleLog("ending retry process at iteration {} since skipped jobs remains at {}.".format(i+1,last_skipped_count))
                    break
            else:
                no_change = 0
            
            keywords_list = keywords_list + skip_keywords
            consoleLog('pausing...')
            pause(5, force=True)
        
        # final summary
        consoleLog('==== final summary (after retry attempts) ====')
        consoleLog('Jobs that couldnt be resolved:')
        consoleLog(skipped_jobs)
    
    if saveOutput:
        today = datetime.today().strftime('%Y-%m-%d')
        writeToJSON(keywords_list, len(jobIDs) - len(skipped_jobs), today)

    freq_dist = getFreqDist(keywords_list)
    return freq_dist
    
        

def mainWorkflow(jobIDs):
    'performs the main web scraping workflow and returns the data'
    (keywords_list, summary_info) = scrapeJobs(jobIDs)

    (data_included, len_data, skipped_jobs) = summary_info
    if (CONFIG.debug_mode):
        freq_dist = getFreqDist(keywords_list)
        summarizeResults(freq_dist, data_included, len_data)

    return (keywords_list, skipped_jobs)

def scrapeJobs(jobIDs):
    'scrapes the data for the given jobIDs'
    skippedJobs = set()
    keywords_list = []

    data_included_count = 0
    step = 0
    time_avg = 0
    begin = time.perf_counter()

    for jobID in jobIDs:
        step += 1
        start = time.perf_counter()
        jobData = getJobData(jobID)
        time_avg += (time.perf_counter() - start)
        if jobData[0] is False:
            if (CONFIG.english_only and jobData[1] == 'non-english'):
                if (CONFIG.debug_mode):
                    print('non-english: {}'.format(jobID))
                continue
            if (CONFIG.debug_mode):
                print('no job data found for [{}]'.format(jobID))
                print('reason: {}'.format(jobData[1]))
            skippedJobs.add(jobID)
            continue
        
        keywords = jobData[1]
        data_included_count += 1

        # keywords
        keywords_list = keywords_list + keywords

        if (step % 10 == 0):
            consoleLog('progress: {}% ({}/{})'.format(round(step/len(jobIDs)*100), step, len(jobIDs)))
            elapsed = round(time.perf_counter() - begin)
            consoleLog('time elapsed: {}s ({}m)'.format(elapsed,round(elapsed / 60)))
    
    if (time_avg > 0):
        time_avg = round(time_avg / len(jobIDs) * 100) / 100
        consoleLog('average time per job: {} seconds'.format(time_avg))
    summary_info = (data_included_count, len(jobIDs), skippedJobs)
    return (keywords_list, summary_info)



def getJobIDs():
    'gets job IDs for linked in job postings'

    jobIDs = set()

    for keyword in CONFIG.keywords:
        done = False
        i = 0
        consoleLog("Getting job IDs for '{}'".format(keyword))

        # number of attempts to reload a URL
        attempts = 0
        max_attempts = 5

        while not done:
            #load each page of results, and get all the job IDs from it
            fmtUrl = getSearchURL(keyword, i, CONFIG.location)
            consoleLog('jobs found: {}'.format(len(jobIDs)))
            consoleLog('fetching job IDs from linkedIn at: {}'.format(fmtUrl))
            res = requestURL(fmtUrl)
            # handle for if connection fails for some reason
            if res[0] is False:
                continue
            res = requests.get(fmtUrl)
            soup = BeautifulSoup(res.text, 'html.parser')

            jobDivs = soup.find_all(class_='base-card')

            # no jobs are found?
            if (len(jobDivs) == 0):
                # if the URL returned nothing, try reloading it again a few times
                if (len(jobIDs) < CONFIG.min_job_count) and (attempts < max_attempts):
                    attempts += 1
                    consoleLog('retrying jobIDs url: attempt {}'.format(attempts))
                    pause(1, force=True)
                    continue
                done = True
                break
            # reset attempts if we succeed in getting a valid URL
            if (attempts > 0):
                consoleLog('succeeded in getting url finally!')
                attempts = 0

            for div in jobDivs:
                jobID = div.get('data-entity-urn').split(":")[3]
                jobIDs.add(jobID)
            
            i = i + 25 # 25 jobs per results page

    if (CONFIG.debug_mode):
        print(jobIDs)
    return jobIDs

def getJobData(jobID):
    '''gets the data for a given job ID'''
    consoleLog('current jobID: {}'.format(jobID))
    retry = 0
    max_retry = 2
    fmtUrl = JOB_URL.format(jobID)
    descriptionSection = None

    # retry getting the job data if it fails
    while ((descriptionSection == None) and (retry < max_retry)):
        res = requestURL(fmtUrl)
        # handle for if connection fails for some reason
        if res[0] is False:
            return res
        soup = BeautifulSoup(res[1], 'html.parser')
        descriptionSection = soup.find(class_=classNames.description)
        retry += 1
        if (descriptionSection == None):
            consoleLog('failed to load job data - trying again')
            pause(1, force=True)
    if (descriptionSection == None):
            consoleLog(soup)
            return (False, 'couldnt find description section')
    
    qualifications = getQualifications(descriptionSection)
    return qualifications


def requestURL(url):
    'Try to fetch the URL, and handle if the connection fails'
    try:
        res = requests.get(url, timeout=10)
    except:
        errmsg = 'connection error: Failed to connect to {}'.format(url)
        if (CONFIG.debug_mode):
            print(errmsg)
        return (False, errmsg)
    
    return (True, res.text)


def getQualifications(description):
    'retrieves data from the description section of the job posting'
    # clean the description of unwanted tags that might interfere
    for e in description.findAll('br'):
        e.extract()
    for e in description.findAll('strong'):
        e.extract()

    # first try searching for list tags
    tags = findListTags(description)
    if tags == None:
        tags = findPTags(description)
    if tags == None:
        return (False, 'No list or p tags could be found in description.')
    
    # if that fails, try searching for p tags
    output = searchTags(tags)
    return output


def searchTags(tags):
    'search the tags for text and parse out keywords.'
    keyword_set = set()

    # check bullet points for tech terms and other useful information
    for tag in tags:
        s = findString(tag)
        if (s == None):
            if (CONFIG.debug_mode):
                print('empty tag?')
                print(tag)
                print('if there are any child tags, they should be removed or traversed.')
            continue

        if (CONFIG.english_only and isForeignScript(s)):
            return (False, 'non-english')
        
        # find keywords
        keywords = stripJunk(s)
        keyword_set = keyword_set.union(keywords)
    
    return (True, list(keyword_set))

def findListTags(description):
    'finds <li> tags in the description'
    ul_tag = description.find('ul')
    if ul_tag == None:
        return None
    all_li = ul_tag.findAll('li')
    return all_li
    
def findPTags(description):
    'finds <p> tags in the description'
    ptags = description.findAll('p')
    return ptags

def findString(tag):
    'try to find a string in the given tag or its children'
    s = tag.string
    if (s != None):
        return s
    
    # if there are children elements, look through them for strings
    if (tag.children != None):
        children = list(tag.children)
        if len(children) >= 1:
            # do search
            s = ''
            for child in children:
                if type(child) == element.NavigableString:
                    s += ' ' + child
                if child.string != None:
                    s += ' ' + child.string
            return s
    
    # otherwise, try the next child - sometimes there are empty tags next to navigable strings (no clue why)
    return tag.nextSibling
    

# strips all "junk" from an input string and returns the keywords in a set
# expects some form of common language input.
# ex: 
# input ->  "preferred: deep understanding of python, javascript, and mySQL"
# output -> {'python', 'javascript', 'mySQL'}
def stripJunk(s):
    'parses out keywords from a raw string'
    if (s == None):
        return set()
    if (type(s) != element.NavigableString):
        return set()

    # there must be at least some ascii characters, even if non-english
    s = removeNonLatinText(s)
    if len(s) == 0:
        return set()
    
    s = s.lower()
    s = ', or '.join(s.split('/')) # replace / with ', or ' so they are seen as separate terms by NLTK

    # find any existing save words - words we want to intercept and save regardless of what NLTK thinks
    exclude = {',', ':', ';', '!', '(', ')', '[', ']'} # cut out these punc
    temp = ''.join(ch for ch in s if ch not in exclude)
    # find phrases in the string that might include spaces
    # note: this may add performance slowdown since we are doing more iteration and checking for substrings here
    skip = set()
    savePhrases = []
    for phrase in SAVE_PHRASES:
        if phrase in temp:
            skip = skip.union(set(phrase.split())) # don't count this word individually since its part of a phrase
            savePhrases.append(phrase)
    saveWords = [word for word in temp.split() if word in SAVE_WORDS]

    ignore = skip.union(IGNORE)

    # NLTK tries to find nouns (usually pretty well!)
    tokenized = [word for word in nltk.word_tokenize(s)]
    tagged = nltk.pos_tag(tokenized)
    nouns = [lemmatize(word) for (word, pos) in tagged if 'NN' in pos]

    # combine our saveWords and NLTK's nouns
    # remove stop words or ignore words, and then conflate any terms into
    # their preferred forms
    allTheWords = nouns + saveWords + savePhrases
    conflated = []
    for word in allTheWords:
        if (word in ignore):
            continue
        if (word in STOP):
            continue
        if (word in CONFLATE):
            conflated.append(CONFLATE[word])
        else:
            conflated.append(word)

    output = set(conflated)

    if (CONFIG.debug_mode and DEBUG.find_terms):
        intersect = DEBUG.find_list.intersection(output)
        if len(intersect) > 0:
            print('Found find_list terms!')
            print(intersect)
            print(s)
            input('press enter to continue: ')

    return output

def lemmatize(word):
    'convert word into singular form'
    # prevent non-words ending with 's' from being lemmatized incorrectly
    if len(word) <= 3:
        return word
    return lemmatizer.lemmatize(word)


def removeNonLatinText(s):
    'removes all characters from non-latin scripts (such as Japanese, Arabic, etc)'
    stripStr = re.sub("[^0-9a-zA-Z,.'+#&*-]",'_', s) # replaces all non alphanumeric (or not ,.) with _
    cleanStr = ''
    lastChar = ''
    for ch in stripStr:
        # when a word switches to _, add a space
        if lastChar != '_':
            if ch == '_':
                cleanStr += ' '
        if ch != '_':
            cleanStr += ch
        lastChar = ch
    return cleanStr.strip()

def isForeignScript(s):
    'detects if the given string is a foreign script or not (non-ascii characters)'
    original_length = len(s)
    stripStr = removeNonLatinText(s)

    # if > 50% of the string is comprised of non-ascii characters, it's probably not english.
    if (len(stripStr) < (original_length / 2)):
        return True
    return False

def getFreqDist(keywords_list):
    freq_keywords = nltk.FreqDist(keywords_list)
    freq_keywords = [(word, freq) for (word, freq) in freq_keywords.most_common() if freq >= CONFIG.keyword_freq]
    return freq_keywords

def summarizeResults(freq_keywords, data_included = 0, len_data = 0):
    'shows data gathered from scraping linkedIn, and also displays a summary information of jobs skipped'

    print('==== Results ====')
    print('\n')
    print('Top 20 keywords:')
    print('\n')
    for (word, freq) in freq_keywords[:20]:
        print('{}: {}'.format(word, freq))
    print('\n')
    print('(All the rest)')
    print(freq_keywords[20:])
    print('\n')

    if (data_included == 0 or len_data == 0):
        return
    print('\n')
    print("== Search info ==")
    print("total jobs found: {}".format(len_data))
    print("jobs searched: {}/{} ({}%)".format(data_included,len_data,round(data_included/len_data*100)))
    print("jobs skipped: {}/{}".format(len_data - data_included,len_data))

def writeToJSON(keywords_list, jobCount, filename):
    'writes the keywords data to a local json file. file will be saved in a ./data/ directory.'
    freq_keywords = nltk.FreqDist(keywords_list)
    freq_keywords = [(word, freq) for (word, freq) in freq_keywords.most_common() if freq >= CONFIG.keyword_freq]
    output = [jobCount] + freq_keywords

    with open('data/{}.json'.format(filename), 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    consoleLog('Saved data to {}.json!'.format(filename))


# functions for testing stuff

def testJob(jobID):
    'test getting data from a given jobID'
    jobData = getJobData(jobID)
    print(jobData)

def testSentence(sentence):
    'test getting keywords from a given sentence string'
    print(sentence)
    print(stripJunk(element.NavigableString(sentence)))

def manualFindIgnore(word_list):
    '''
    function to help you go through the output keywords and mark new ignore terms.
    input the list/set of keywords output from a the search summary and go through each, deciding if it should be ignored or not.
    '''
    ignore_add = set()
    for (word, freq) in word_list:
        if word.lower() in SAVE_WORDS:
            continue
        print('{}: {}'.format(word, freq))
        ans = input('add to ignore? (y/n/x): ')
        if ans.lower() == 'y':
            ignore_add.add(word)
        if ans.lower() == 'x':
            break
    print('new ignore set: ')
    newIgnore = ignore_add.union(IGNORE)
    print(newIgnore)

words = [('C', 56), ('front-end', 54), ('docker', 53), ('Node.js', 51), ('RESTful API', 48), ('linux', 47), ('.NET', 46), ('AWS', 45), ('microservices', 45), ('full stack', 44), ('scrum', 43), ('ci cd', 42), ('swift', 38), ('Go', 36), ('kubernetes', 36), ('scientist', 34), ('jenkins', 33), ('Machine Learning', 32), ('Azure', 32), ('jira', 32), ('oracle', 32), ('architect', 30), ('qa', 29), ('analyst', 29), ('devops', 29), ('sprint', 24), ('php', 24), ('Vue.js', 23), ('redux', 22), ('json', 20), ('Visual Studio', 20), ('Google Cloud', 19), ('sdlc', 19), ('terraform', 19), ('saas', 18), ('github', 18), ('Artificial Intelligence', 17), ('iac', 17), ('polygraph', 16), ('iOS', 16), ('android', 16), ('OOP', 16), ('html5', 15), ('milestone', 15), ('jquery', 15), ('person', 14), ('unix', 14), ('gitlab', 14), ('manufacturing', 14), ('mvc', 14), ('minute', 13), ('xml', 13), ('ms', 13), ('startup', 13), ('NoSQL', 13), ('aid', 13), ('serverless', 13), ('slack', 12), ('kafka', 12), ('visualization', 12), ('space', 12), ("Master's Degree", 12), ('sci', 12), ('mathematics', 12), ('modeling', 12), ('css3', 11), ('pas', 11), ('greenfield', 11), ('audience', 11), ('modernization', 11), ('cross', 11), ('class', 11), ('accounting', 11), ('j2ee', 11), ('stem', 11), ('connection', 10), ('micro', 10), ('cms', 10), ('data analysis', 10), ('junior', 10), ('finding', 10), ('author', 10), ('bar', 10), ('legacy', 10), ('junit', 10), ('Ruby', 10), ('flask', 10), ('vehicle', 10), ('check', 10), ('postgres', 10), ('theory', 9), ('asp.net', 9), ('lab', 9), ('course', 9), ('artifact', 9), ('mongodb', 9), ('statement', 9), ('rail', 9), ('graphql', 9), ('file', 9), ('post-release', 9), ('phone', 9), ('offering', 9), ('trading', 9), ('fulfillment', 9), ('internship', 9), ('parental', 9), ('elder', 9), ('tutoring', 9), ('containerization', 8), ('equity', 8), ('train', 8), ('repair', 8), ('elasticsearch', 8), ('redis', 8), ('downtime', 8), ('dod', 8), ('provider', 8), ('hiring', 8), ('reuse', 8), ('amazon', 8), ('intern', 8), ('desktop', 8), ('google', 8), ('http', 8), ('UX', 8), ('entity', 8), ('b.s', 8), ('truecommerce', 8), ('writer', 8), ('school', 8), ('shell', 8), ('bitbucket', 8), ('physic', 8), ('sustainment', 8), ('configure', 8), ('refactor', 8), ('ease', 8), ('summer', 8), ('path', 8), ('relief', 8), ('cryopreservation', 8), ('child', 8), ('disaster', 8), ('surrogacy', 8), ('adapt', 7), ('generate', 7), ('gui', 7), ('researcher', 7), ('chart', 7), ('memory', 7), ('devsecops', 7), ('anticipate', 7), ('subsystem', 7), ('salesforce', 7), ('debugs', 7), ('autonomy', 7), ('number', 7), ('aircraft', 7), ('eclipse', 7), ('networking', 7), ('awareness', 7), ('york', 7), ('division', 7), ('matlab', 7), ('video', 7), ('django', 7), ('origin', 7), ('excel', 7), ('verbal', 7), ('fast', 7), ('gain', 7), ('iteration', 7), ('implementing', 7), ('automate', 7), ('scaling', 7), ('solving', 7), ('fun', 7), ('figma', 7), ('wordpress', 7), ('thinking', 7), ('extension', 7), ('tuition', 7), ('curiosity', 7), ('compiler', 7), ('correctness', 7), ('everything', 7), ('schema', 7), ('budget', 6), ('endpoint', 6), ('resiliency', 6), ('writes', 6), ('apache', 6), ('processor', 6), ('measurement', 6), ('interoperability', 6), ('tester', 6), ('friday', 6), ('rotation', 6), ('Ruby-on-Rails', 6), ('lockheed', 6), ('full-time', 6), ('martin', 6), ('driven', 6), ('judgment', 6), ('trade', 6), ('micro-services', 6), ('us', 6), ('patient', 6), ('portion', 6), ('math', 6), ('agency', 6), ('instrument', 6), ('veteran', 6), ('powerpoint', 6), ('secret', 6), ('retrospective', 6), ('robustness', 6), ('b', 6), ('observability', 6), ('sc', 6), ('dev', 6), ('oversight', 6), ('item', 6), ('identification', 6), ('microservice', 6), ('desk', 6), ('db2', 6), ('batch', 6), ('age', 6), ('tuning', 6), ('codebases', 6), ('feel', 6), ('dive', 6), ('experimentation', 6), ('discovery', 6), ('apple', 6), ('aerospace', 6), ('topic', 6), ('full-stack', 6), ('front', 6), ('selection', 6), ('graduate', 6), ('contact', 6), ('bootstrap', 6), ('specialist', 6), ('suggestion', 6), ('compliant', 6), ('game', 6), ('listella', 5), ('jest', 5), ('shoot', 5), ('performant', 5), ('meta', 5), ('format', 5), ('inclusion', 5), ('act', 5), ('inception', 5), ('characteristic', 5), ('perspective', 5), ('robotics', 5), ('intelligence', 5), ('proof', 5), ('audit', 5), ('board', 5), ('hook', 5), ('servlets', 5), ('graphic', 5), ('flight', 5), ('clarity', 5), ('remote', 5), ('launch', 5), ('firmware', 5), ('mitigation', 5), ('history', 5), ('compensation', 5), ('top', 5), ('investment', 5), ('america', 5), ('art', 5), ('puppet', 5), ('letter', 5), ('supply', 5), ('sw', 5), ('regard', 5), ('latency', 5), ('sharing', 5), ('logging', 5), ('modifies', 5), ('kind', 5), ('hadoop', 5), ('kanban', 5), ('rust', 5), ('index', 5), ('progeny', 5), ('word', 5), ('bash', 5), ('sharepoint', 5), ('pressure', 5), ('jboss', 5), ('combination', 5), ('time-series', 5), ('eye', 5), ('advantage', 5), ('workshop', 5), ('forefront', 5), ('livesite', 5), ('oo', 5), ('servicing', 5), ('solve', 5), ('sas', 5), ('chain', 5), ('rdbms', 5), ('capture', 5), ('attend', 5), ('springboot', 5), ('selenium', 5), ('flowchart', 5), ('electronics', 5), ('conflict', 5), ('posse', 5), ('mentality', 5), ('mean', 5), ('install', 5), ('soap', 5), ('ide', 5), ('programmer', 5), ('inventory', 5), ('ops', 5), ('lambda', 5), ('dynamodb', 5), ('union', 5)]
manualFindIgnore(words)