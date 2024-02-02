import re

from bs4 import BeautifulSoup, element

from request_url import requestUrl, JOB_URL
from config import consoleLog, pause, config as CONFIG
from engine import run_engine

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

# ==============================
#
# Parsing job search pages
#
# ==============================

def parseJobIDsFromPage(text):
    soup = BeautifulSoup(text, 'html.parser')
    jobDivs = soup.find_all(class_='base-card')
    jobIDs = set()

    # if there are no jobs, we probably got an invalid response from the request and should retry
    if (len(jobDivs) == 0):
        return False, jobIDs

    for div in jobDivs:
        jobID = div.get('data-entity-urn').split(":")[3]
        jobIDs.add(jobID)
    
    return True, jobIDs

# ==============================
#
# Parsing job description pages
#
# ==============================

async def getJobData(jobID):
    '''gets the data for a given job ID'''
    # find the description section - this will hold all the useful information
    descriptionSection = await getDescriptionSection(jobID)
    if descriptionSection == None:
        return None

    # find tags to search for data
    tags = findSearchableTagsInDescription(descriptionSection)
    if tags == None:
        return None
    
    # find keyword data in the tags
    keywords_list = searchTags(tags)
    return keywords_list

async def getDescriptionSection(jobID):
    'attempts to find a description section for the given job ID'
    attempts = 0
    maxAttempts = 2
    fmtUrl = JOB_URL.format(jobID)
    descriptionSection = None

    # retry getting the job data if it fails
    while ((descriptionSection == None) and (attempts < maxAttempts)):
        attempts += 1
        res = await requestUrl(fmtUrl)

        # retry if connection fails
        if res[0] is False:
            continue

        # try to extract the description section from the response
        soup = BeautifulSoup(res[1], 'html.parser')
        descriptionSection = soup.find(class_=classNames.description)

        # retry if response is bad
        if (descriptionSection == None):
            pause(1, force=True)
    
    return descriptionSection

def findSearchableTagsInDescription(description):
    # clean the description of unwanted tags that might interfere
    for e in description.findAll('br'):
        e.extract()
    for e in description.findAll('strong'):
        e.extract()

    # first try searching for list tags
    tags = findListTags(description)
    # if that fails, try finding p tags. 
    # these tend to have less useful data and may just be high level job descriptions
    if tags == None:
        tags = findPTags(description)
    return tags


def searchTags(tags):
    'search the tags for text and parse out a list of keywords.'
    keyword_set = set()

    # check bullet points for tech terms and other useful information
    for tag in tags:
        s = findString(tag)
        if (s == None):
            continue

        if (CONFIG.english_only and isForeignScript(s)):
            return []
        
        # find keywords
        keywords = stripJunk(s)
        keyword_set = keyword_set.union(keywords)
    
    return list(keyword_set)

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

# ==============================
#
# General Utils
#
# ==============================

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