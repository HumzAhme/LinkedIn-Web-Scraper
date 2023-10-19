from bs4 import BeautifulSoup
import requests
import time
import re
import nltk
from nltk.corpus import stopwords
import ssl
import string
import time
from terms import IGNORE


# workaround to get nltk to work...
# https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

nltk_stop = set(stopwords.words('english'))

# words to strip without allowing potential analysis.
# ex: if 'admin' by itself isn't useful, but 'linux admin' is, don't put 'admin' here.
# instead, put it in the IGNORE list
my_stop = {
    'join','level','review','content','builder','detail','liaise','evaluating','make','~','’'
}
STOP = nltk_stop.union(my_stop)

# Data to get:
#
# freq of company | ?
# freq of job title | ?
# freq of seniority level | ?
# years of experience freq range | Done
# freq of programming languages | Done
# freq of other tech concepts/key words | Done

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

# preferred names for conflated terms
javascript = 'Javascript'
typescript = 'Typescript'
node = 'Node.js'
react = 'React.js'
vue = 'Vue.js'
angular = 'Angular.js'
golang = 'Go'
oop = 'OOP'
frontend = 'front-end'
backend = 'back-end'
rails = 'Ruby-on-Rails'
dotnet = '.NET'

# terms to conflate into a singular preferred form
# since there are many ways a given concept may be written, we conform
# them all using this dictionary
CONFLATE = {
    # javascript/typescript
    'js': javascript,
    'ts': typescript,
    # react
    'react': react,
    'reactjs': react,
    'react.js': react,
    # vue
    'vuejs': vue,
    'vue': vue,
    'vue.js': vue,
    # angular
    'angular': angular,
    'angularjs': angular,
    'angular.js': angular,
    #node
    'node': node,
    'nodejs': node,
    'node.js': node,
    # golang
    'golang': golang,
    'go.lang': golang,
    # ruby-on-rails
    'ruby-on-rails': rails,
    'ruby on rails': rails,
    'rails': rails,
    # .NET
    '.net': dotnet,
    '.NET': dotnet,
    # misc
    'restful': 'RESTful',
    'oop': oop,
    'OOP': oop,
    'object-oriented': oop,
    'object-oriented-programming': oop,
    'object oriented': oop,
    'object oriented programming': oop,
    'frontend': frontend,
    'front-end': frontend,
    'backend': backend,
    'back-end': backend
}

# phrases or terms that includes spaces - since sentences are split by spaces, we try to intercept these terms first
PHRASES = [
    'back end',
    'front end',
    'object oriented',
    'ruby on rails',
    'site reliability',
    'machine learning',
    'data mining',
    'artificial intelligence',
    'data analysis',
    'unit test',
    'computer science',
    'bachelor degree',
    "batchelors degree",
    'master degree',
    "masters degree",
    'system administrator',
    'full stack',
    'team lead',
    'senior engineer',
    'senior developer',
    'junior engineer',
    'junior developer',
    'web developer',
    'application developer',
    'application engineer',
    'mobile developer',
    'google cloud platform',
    'amazon web service',
    'rest api',
    'rest apis',
    'system engineer'
]


KEYWORD = 'Software Developer'
LOCATION = 'Tokyo, Japan'

SEARCH_URL = 'https://www.linkedin.com/jobs/search/?keywords={0}&location={1}&start={2}'
JOB_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'

#nltk.download('words')
#WORDS = set(nltk.corpus.words.words())

# tech words we want to make sure aren't ignored or stripped by NLTK logic by accident
# our logic ideally allows any noun-like terms (that aren't stop words/ignored) to go through
# but sometimes weird things happen, so just to be safe I am listing popular terms or ones that may potentially be erroneously ignored.
TECH_WORDS = {
    'react','react.js','assembly','git','cloud','angular','angular.js','c#','c++','mobile','android','ios','oop','object-oriented',
    'node','node.js','restful','go','golang','.net','linux','unix','macos','windows','web3','github','nosql','mysql','sql','aws','gcp',
    'bash','kernel'
}

# misc words to ignore - mostly random tech terms and corporate speak that may commonly appear in JDs



def scrapeLinkedIn():
    jobIDs = getJobIDs()
    
    (years_of_exp, keywords_list, skipped_jobs) = mainWorkflow(jobIDs)

    # if there were any skipped jobs, try re-doing them
    if (len(skipped_jobs) > 0):
        retry = 5
        time.sleep(2)

        print('Some jobs ({}/{}) failed. Do you want to retry them?'.format(len(skipped_jobs), len(jobIDs)))
        print('(Note: this code will retry {} times, or until no more skipped jobs are getting resolved)'.format(retry))
        ans = input('Y/N: ')
        if (ans.lower() != 'y'):
            return
        
        for i in range(retry):
            last_skipped_count = len(skipped_jobs)
            (skip_years_exp, skip_keywords, skipped_jobs) = mainWorkflow(skipped_jobs)
            if (last_skipped_count == len(skipped_jobs)):
                print('ending retry process at iteration {}; no skipped jobs were resolved since last iteration ({}).'.format(i+1,last_skipped_count))
                break
            # merge the years-of-experience dictionaries
            for year in skip_years_exp:
                if year in years_of_exp:
                    years_of_exp[year] += skip_years_exp[year]
                else:
                    years_of_exp[year] = skip_years_exp[year]
            keywords_list = keywords_list + skip_keywords
            print('pausing...')
            time.sleep(5)
            print('restart!')
            time.sleep(0.5)
        
        # final summary
        print('==== final summary (after retry attempts) ====')
        summarizeResults(years_of_exp, keywords_list)
        

def mainWorkflow(jobIDs):
    'performs the main web scraping workflow and returns the data'
    (years_of_exp, keywords_list, summary_info) = scrapeJobs(jobIDs)

    (data_included, len_data, skipped_jobs) = summary_info
    summarizeResults(years_of_exp, keywords_list, data_included, len_data)

    return (years_of_exp, keywords_list, skipped_jobs)

def scrapeJobs(jobIDs):
    'scrapes the data for the given jobIDs'
    skippedJobs = []

    years_of_exp = {}
    keywords_list = []

    data_included_count = 0
    step = 0

    for jobID in jobIDs:
        step += 1
        jobData = getJobData(jobID)
        if (jobData == None):
            print('no job data found for [{}]'.format(jobID))
            skippedJobs.append(jobID)
            continue
        exp = jobData[0]
        keywords = jobData[1]
        data_included_count += 1

        # years of experience
        if (exp in years_of_exp):
            years_of_exp[exp] += 1
        else:
            years_of_exp[exp] = 1
        # keywords
        keywords_list = keywords_list + keywords

        if (step % 10 == 0):
            print('progress: {} percent ({}/{})'.format(step/len(jobIDs)*100, step, len(jobIDs)))
    
    summary_info = (data_included_count, len(jobIDs), skippedJobs)
    return (years_of_exp, keywords_list, summary_info)

def summarizeResults(years_of_exp, keywords_list, data_included = 0, len_data = 0):
    'shows data gathered from scraping linkedIn, and also displays a summary information of jobs skipped'

    freq_keywords = nltk.FreqDist(keywords_list)

    print('==== Results ====')
    print('\n')
    print('Frequency of keywords')
    print('\n')
    print(freq_keywords.most_common())
    print('\n')
    print('Frequency of years experience requirements')
    print('\n')
    print(years_of_exp)
    print('\n')

    if (data_included == 0 or len_data == 0):
        return
    print('\n')
    print("== Search info ==")
    print("total jobs found: {}".format(len_data))
    print("jobs searched: {}".format(data_included/len_data*100))
    print("jobs skipped: {}".format((len_data - data_included)/len_data*100))

def getJobIDs():

    timeLimit = 60

    done = False
    i = 0
    jobIDs = []

    startTime = time.perf_counter()
    print("Getting job IDs")

    while not done:
        #load each page of results, and get all the job IDs from it
        fmtUrl = SEARCH_URL.format(KEYWORD, LOCATION,i)
        print('fetching job IDs from linkedIn at: {}'.format(fmtUrl))
        res = requests.get(fmtUrl)
        soup = BeautifulSoup(res.text, 'html.parser')

        jobDivs = soup.find_all(class_='base-card')

        if (len(jobDivs) == 0):
            done = True
            break

        # cut it off if code takes too long
        #if (i % 100 == 0):
        #    if (time.perf_counter() - startTime > timeLimit):
        #        done = True
        #        break

        for div in jobDivs:
            jobID = div.get('data-entity-urn').split(":")[3]
            jobIDs.append(jobID)
        
        i = i + 25 # 25 jobs per results page

    return jobIDs

def getJobData(jobID):

    fmtUrl = JOB_URL.format(jobID)
    res = requests.get(fmtUrl)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    descriptionSection = soup.find(class_=classNames.description)
    if (descriptionSection == None):
        print(' . . [no desc]')
        #print(soup)
        return None
    qualifications = getQualifications(descriptionSection)

    if qualifications != None:
        if qualifications[0] > 10:
            print('High YOE found: {}y [{}]'.format(qualifications[0], jobID))

    return qualifications


def getQualifications(description):
    keyword_set = set()

    # find a <strong> tag with words like "qualification(s)", "requirement(s)"
    # from there, find the ul that has all the li bullet points of qualifications
    qual = description.find(string=re.compile('qualification', re.I))
    if qual == None:
        qual = description.find(string=re.compile('requirement', re.I))
    if qual == None:
        print(' . [cant find qualifications]')
    
    # there should be a ul tag where all the description data is listed in bullet points
    if qual == None:
        ul_tag = description.find('ul')
    else:
        ul_tag = qual.parent.findNext('ul')
    if ul_tag == None:
        print(' . . [cant find ul tag]')
        return None
    all_li = ul_tag.findAll('li')

    # get list of each bullet point that includes years experience
    max = 0
    if qual != None:
        li_yearsExp = ul_tag.findAll(string=re.compile('year', re.I))
        # get the max year listed
        # if max remains 0, then no year data was found
        for li in li_yearsExp:
            stripStr = re.sub('[^0-9]','_', li)
            nums = [n for n in stripStr.split('_') if n != '']
            for n in nums:
                if int(n) > max:
                    max = int(n)
            keywords = stripJunk(li)
            keyword_set = keyword_set.union(keywords)

    # check other bullet points for tech terms too
    for li in all_li:
        keywords = stripJunk(li.string)
        keyword_set = keyword_set.union(keywords)

    return (max, list(keyword_set))
    

# strips all "junk" from an input string and returns the keywords in a set
# expects some form of common language input.
# ex: 
# input ->  "preferred: deep understanding of python, javascript, and mySQL"
# output -> {'python', 'javascript', 'mySQL'}
def stripJunk(s):
    if (s == None):
        return set()
    # don't allow non english/latin script text
    if isNonLatinText(s):
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
    for phrase in PHRASES:
        if phrase in temp:
            skip = skip.union(set(phrase.split())) # don't count this word individually since its part of a phrase
            savePhrases.append(phrase)
    saveWords = [word for word in temp.split() if word in TECH_WORDS]

    ignore = skip.union(IGNORE)

    # NLTK tries to find nouns (usually pretty well!)
    tokenized = [word for word in nltk.word_tokenize(s) if not word in ignore] # cut ignore words
    clean1 = [word for word in tokenized if word not in STOP]
    tagged = nltk.pos_tag(clean1)
    nouns = [word for (word, pos) in tagged if 'NN' in pos]

    # combine our saveWords and NLTK's nouns
    # also conflate any similar terms that should be seen as the same thing
    allTheWords = nouns + saveWords + savePhrases
    conflated = []
    for word in allTheWords:
        if (word in CONFLATE):
            conflated.append(CONFLATE[word])
        else:
            conflated.append(word)

    output = set(conflated)
    return output


def isNonLatinText(s):
    'determines if the given string has non-latin characters (such as Japanese, Arabic, etc)'
    return ord(s[0]) > 128



def testJob(jobID):
    jobData = getJobData(jobID)
    print(jobData)


#testJob(3665915576)

#print(stripJunk("join a team focused on database technologies and troubleshoot projects"))

scrapeLinkedIn()