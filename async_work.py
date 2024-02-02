import time
import asyncio
import aiohttp
from parsing import parseJobIDsFromPage


SEARCH_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={0}'
JOB_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
ITER = 3

def getSearchURL(keyword, start = 0, location = None):
    'returns a URL for the job ID search HTTP request'
    url = SEARCH_URL.format(keyword)

    if (location != None):
        url = url + '&location={}'.format(location)
    
    url = url + '&start={}'.format(start)
    return url

async def requestUrl(url):
    'Try to fetch the URL asynchronously and handle connection errors'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10, ssl=False) as response:
                text = await response.text()
                return (True, text)
    except aiohttp.ClientError as e:
        errmsg = f'Connection error: Failed to connect to {url} - {str(e)}'
        print(errmsg)
        return (False, errmsg)
    except asyncio.TimeoutError:
        timeout_msg = f'Timeout error: Connection to {url} timed out.'
        print(timeout_msg)
        return (False, timeout_msg)
    except Exception as e:
        generic_msg = f'Unexpected error: {str(e)}'
        print(generic_msg)
        return (False, generic_msg)

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


async def getJobIDsFromURLs(URLs: list[str], workerID: int | None = None):
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
# General Util
#
# ==========================================================================================================

def getAverageTime(totalTime, iter = 1) -> float:
    return round(totalTime / iter * 1000) / 1000