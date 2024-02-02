import aiohttp
import asyncio

SEARCH_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={0}'
JOB_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'

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