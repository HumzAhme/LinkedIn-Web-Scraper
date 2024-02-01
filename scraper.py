from bs4 import BeautifulSoup, element
import requests
import time
import re
import ssl
import time
from socket import error
import json
import os
from datetime import datetime
from config import config as CONFIG, debugger as DEBUG

from engine import getFreqDist, run_engine

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

def scrapeLinkedIn(test_IDs = None):
    '''
    Entry point for running the linked-in web scraper.
    Returns a frequency distribution of format: [(word, freq), (word2, freq), ...].

    test_IDs: list of job IDs to use for testing - skips the getJobIDs step.
    saveOutput: boolean to toggle if output should be saved to a json. json is saved to ./data/ directory.
    '''
    # display config
    print('=== config ===')
    if (CONFIG.debug_mode):
        print('DEBUG MODE: on')
        if (DEBUG.find_terms):
            print('FIND TERMS: on')
            print('Searching for these terms:')
            print(DEBUG.find_list)
    if (CONFIG.test_run):
        print('TEST RUN! Results will be limited to speed up search.')
    print('\n(To change settings, edit config.py)')
    print('==============')
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

            if (len(skipped_jobs) == 0):
                consoleLog('all jobs searched!')
                break
            consoleLog('pausing...')
            pause(5, force=True)
        consoleLog('Jobs that couldnt be resolved:')
        consoleLog(skipped_jobs)
    
    freq_keywords = getFreqDist(keywords_list)
    jobCount = len(jobIDs) - len(skipped_jobs)
    filtered = filterResults(freq_keywords, jobCount)
    output = [jobCount] + filtered

    filename = datetime.today().strftime('%Y-%m-%d')
    if (CONFIG.test_run):
        filename = f'{filename}_test'
    writeToJSON(output, filename)
    return (output, filename)
    
def filterResults(data, jobCount):
    'does final filtering to remove unnecessary data'
    filtered = []
    for term in data:
        if term[1] / jobCount < CONFIG.freq_threshold:
            continue
        filtered.append(term)
    return filtered

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
                attempts += 1
                continue
            soup = BeautifulSoup(res[1], 'html.parser')

            jobDivs = soup.find_all(class_='base-card')

            # no jobs are found?
            if (len(jobDivs) == 0):
                # if the URL returned nothing, try reloading it again a few times
                if (attempts < max_attempts):
                    attempts += 1
                    consoleLog('retrying jobIDs url: attempt {}'.format(attempts))
                    pause(1, force=True)
                    continue
                done = True
                break
            # reset attempts if we succeed in getting a valid URL
            if (attempts > 0):
                consoleLog('succeeded in getting url finally! ({} attempts)'.format(attempts))
                attempts = 0

            for div in jobDivs:
                jobID = div.get('data-entity-urn').split(":")[3]
                jobIDs.add(jobID)
            
            if (CONFIG.test_run):
                if len(jobIDs) >= 300:
                    break
            i = i + 25 # 25 jobs per results page

        if (CONFIG.test_run):
            if len(jobIDs) >= 300:
                break

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
            #consoleLog(soup)
            return (False, 'couldnt find description section')
    
    qualifications = getQualifications(descriptionSection)
    return qualifications


def requestURL(url):
    'Try to fetch the URL, and handle if the connection fails'
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
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
    if type(tag.nextSibling) == "NavigableString":
        return tag.nextSibling
    return None
    

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
        s = element.NavigableString(s)

    # there must be at least some ascii characters, even if non-english
    s = removeNonLatinText(s)
    if len(s) == 0:
        return set()
    
    output = run_engine(3, s)

    # also use the term finder - on the unrestricted list of terms though
    #if (CONFIG.debug_mode and DEBUG.find_terms):
    #    intersect = DEBUG.find_list.intersection(set(allTheWords))
    #    if len(intersect) > 0:
    #        print('Found find_list terms!')
    #        print(intersect)
    #        print(s)
    #        writeToLog(str(intersect))
    #        writeToLog(s)
    return output

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

def writeToJSON(data, filename):
    'writes the keywords data to a local json file. file will be saved in a ./data/ directory.'
    filepath = 'data/{}.json'.format(filename)
    os.makedirs('./data', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    consoleLog('Saved data to {}.json!'.format(filename))

def writeToLog(s):
    with open('log.txt', 'a') as f:
        f.write('\n'.join(s))

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
        if word.lower() in IGNORE:
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