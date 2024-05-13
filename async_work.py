import time
import asyncio
from parsing import parseJobIDsFromPage, getJobData
from request_url import getSearchURL, requestUrl
from typing import List, Optional


ITER = 3
    
# ==========================================================================================================
#
# Searching Job IDs
#
# ==========================================================================================================

def getJobSearchURLs(keyword: str):
    'gets a list of URLs representing searching for jobs based on a keyword. Used for finding job IDs.'
    URLs = []
    i = 0
    # seems it can fetch job IDs until i=1000
    while i <= 1000:
        URLs.append(getSearchURL(keyword, i))
        i += 25 # 25 per page
    return URLs

def pause():
    time.sleep(1)

async def getJobIDsAsync(keyword: str):
    '''
    Gets searches for jobs based on the given keyword and returns a set of found job IDs.

    Splits the searching and parsing load between a set of "workers" which work in parallel,
    dramatically improving performance compared to doing all the work synchronously.
    '''
    URLs = getJobSearchURLs(keyword)

    # split the load into tasks for workers
    numWorkers = 4
    chunkSize = len(URLs) // numWorkers
    chunks = [URLs[i:i+chunkSize] for i in range(0, len(URLs), chunkSize)]
    tasks = []
    for i, chunk in enumerate(chunks):
        task = asyncio.create_task(getJobIDsFromURLs(chunk, i + 1))
        tasks.append(task)
    
    begin = time.perf_counter()

    results = await asyncio.gather(*tasks)

    jobIDs = set().union(*results)
    
    timeTaken = getAverageTime(time.perf_counter() - begin)
    print(f"Done! took {timeTaken} seconds")
    print(f"Number of job IDs found: {len(jobIDs)}")
    return jobIDs

async def getJobIDsSync(keyword: str):
    '''
    Gets searches for jobs based on the given keyword and returns a set of found job IDs.

    Does the work sequentially, without any parellelism or splitting the load between workers.
    '''
    URLs = getJobSearchURLs(keyword)
    
    begin = time.perf_counter()

    jobIDs = await getJobIDsFromURLs(URLs)
    
    timeTaken = getAverageTime(time.perf_counter() - begin)
    print(f"Done! took {timeTaken} seconds")
    print(f"Number of job IDs found: {len(jobIDs)}")
    return jobIDs


async def getJobIDsFromURLs(URLs: list[str], workerID: int | None = None): # '|' (pipe) is only workable/recognized for python 3.10 and above. if this doesn't work, add instead:
                                                                           # async def getJobIDsFromURLs(URLs: List[str], workerID: Optional[int] = None):
    '''
    Takes a list of job search URLs and attempts to find job IDs from each.

    Pass a workerID in if this is part of an asynchronous approach.
    '''
    # try each URL one at a time, and retry each one a max of 3 times
    jobIDs = set()
    done = False
    attempts = 0
    maxAttempts = 3
    failedJobCount = 0
    requestFailCount = 0

    if workerID != None:
        print(f"START: Worker {workerID} is starting with {len(URLs)} URLs")

    while not done:
        retry = []
        prevSize = len(URLs)

        # try to request the data from each URL
        for url in URLs:
            res = await requestUrl(url)
            if res[0] == False:
                retry.append(url)
                requestFailCount += 1
                await asyncio.sleep(1)
            else:
                dataExists, jobs = parseJobIDsFromPage(res[1])
                if not dataExists:
                    retry.append(url)
                    requestFailCount += 1
                    await asyncio.sleep(1)
                else:
                    jobIDs = jobIDs.union(jobs)
        
        # if no URLs are getting completed, consider it a failed attempt
        if len(retry) == prevSize:
            attempts += 1
        # exit if we are at max attempts
        if attempts >= maxAttempts:
            done = True
        # if there are no URLs to retry, we're done
        if len(retry) == 0:
            done = True
        if not done:
            URLs = retry.copy()
        failedJobCount = len(retry)
    
    if workerID != None:
        print(f"END: Worker {workerID} has finished - found {len(jobIDs)} jobs.")
    #print(f"Failed jobs: {failedJobCount}")
    #print(f"Number of failed request attempts: {requestFailCount}")
    #print(f"Number of jobs found: {len(jobIDs)}")
    return jobIDs

def getJobIDsForListOfKeywords(keywords: list[str], use_async = True) -> set[str]:
    'given a list of keywords, returns jobIDs for jobs found while searching for those keywords.'
    jobIDs = set()

    begin = time.perf_counter()

    if use_async:
        print("Job ID Search: Using async approach")
    else:
        print("Job ID Search: Using sequential approach")

    for keyword in keywords:
        print(f"Finding Job IDs for \"{keyword}\" jobs")
        if use_async:
            newJobIDs = asyncio.run(getJobIDsAsync(keyword))
        else:
            newJobIDs = asyncio.run(getJobIDsSync(keyword))
        print(f"...Done! Found {len(newJobIDs)} jobs")
        jobIDs = jobIDs.union(newJobIDs)
    
    timeTaken = time.perf_counter() - begin
    seconds = round(timeTaken)
    minutes = round(seconds / 60)
    print("==============================================")
    print(f"Job ID search complete: took {seconds} seconds (~{minutes} m)")
    print(f"Found {len(jobIDs)} job IDs!")
    print("==============================================")
    
    return jobIDs

# ==========================================================================================================
#
# Getting Job Data
#
# ==========================================================================================================

def getAllJobData(jobIDs: set[str]):
    return asyncio.run(getJobDataAsync(jobIDs))

async def getJobDataAsync(jobIDs: set[str]):

    jobIDsList = list(jobIDs)
    # split the jobIDs into chunks according to our number of workers
    numWorkers = 4
    chunkSize = len(jobIDsList) // numWorkers
    chunks = [jobIDsList[i:i+chunkSize] for i in range(0, len(jobIDsList), chunkSize)]
    tasks = []
    for i, chunk in enumerate(chunks):
        task = asyncio.create_task(scrapeJobsWorker(chunk, i + 1))
        tasks.append(task)
    
    begin = time.perf_counter()

    results = await asyncio.gather(*tasks)

    # combine all the lists of keywords into one
    keywords_list = []
    data_incl_count = 0
    total_jobs = 0
    skipped_jobs = set()
    for word_list, summary in results:
        keywords_list.extend(word_list)
        data_incl_count += summary[0]
        total_jobs += summary[1]
        skipped_jobs = skipped_jobs.union(summary[2])

    timeTaken = time.perf_counter() - begin
    seconds = round(timeTaken)
    minutes = round(seconds / 60)
    print("==============================================")
    print(f"Job data parsing complete: took {seconds} seconds (~{minutes} m)")
    print("==============================================")

    summary_info = (data_incl_count, total_jobs, skipped_jobs)
    return (keywords_list, summary_info)

async def scrapeJobsWorker(jobIDs: list[str], workerID: int):
    skippedJobs = set()
    keywords_list = []

    data_included_count = 0
    step = 0
    begin = time.perf_counter()
    lastLog = time.perf_counter()

    print(f"START: Worker {workerID} is scraping {len(jobIDs)} jobs.")

    for jobID in jobIDs:
        step += 1
        keywords = await getJobData(jobID)
        if keywords == None:
            skippedJobs.add(jobID)
            continue
        data_included_count += 1
        keywords_list = keywords_list + keywords

        # log progress every minute-ish
        if (step % 10 == 0 and time.perf_counter() - lastLog >= 60):
            lastLog = time.perf_counter()
            perc = round(step/len(jobIDs)*100)
            print(f"Worker {workerID}: {perc}% done ({step}/{len(jobIDs)})")
            elapsed = round(time.perf_counter() - begin)
            print('time elapsed: {}s ({}m)'.format(elapsed,round(elapsed / 60)))
    
    timeTaken = time.perf_counter() - begin
    seconds = round(timeTaken)
    minutes = round(seconds / 60)
    print(f"END: Worker {workerID} finished in {seconds} seconds (~{minutes} m) - skipped {len(skippedJobs)} jobs.")
    summary_info = (data_included_count, len(jobIDs), skippedJobs)
    return keywords_list, summary_info

# ==========================================================================================================
#
# General Util
#
# ==========================================================================================================

def getAverageTime(totalTime, iter = 1) -> float:
    return round(totalTime / iter * 1000) / 1000
