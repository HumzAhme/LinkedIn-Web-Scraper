import time
import json
import os
from datetime import datetime
from config import config as CONFIG, debugger as DEBUG, consoleLog, pause
from engine import getFreqDist
from async_work import getJobIDsForListOfKeywords, getAllJobData


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

def mainWorkflow(jobIDs: set[str]):
    'performs the main web scraping workflow and returns the data'
    (keywords_list, summary_info) = scrapeJobs(jobIDs)

    (data_included, len_data, skipped_jobs) = summary_info
    if (CONFIG.debug_mode):
        freq_dist = getFreqDist(keywords_list)
        summarizeResults(freq_dist, data_included, len_data)

    return (keywords_list, skipped_jobs)

def scrapeJobs(jobIDs: set[str]):
    'scrapes the data for the given jobIDs'
    return getAllJobData(jobIDs)

def getJobIDs() -> set[str]:
    'gets job IDs for linked in job postings'
    keywords = CONFIG.keywords
    jobIDs = getJobIDsForListOfKeywords(keywords)

    return jobIDs

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