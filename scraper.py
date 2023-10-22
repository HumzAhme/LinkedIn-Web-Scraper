from bs4 import BeautifulSoup, element
import requests
import time
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import ssl
import time
import os
from socket import error
from config import config as CONFIG

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

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

lemmatizer = WordNetLemmatizer()

nltk_stop = set(stopwords.words('english'))
STOP_WORDS = nltk_stop.union(STOP)

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


# You can change the search criteria here
KEYWORD = 'Software Developer'
LOCATION = 'Tokyo, Japan'

SEARCH_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={0}&location={1}&start={2}'
JOB_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'


def scrapeLinkedIn():
    jobIDs = getJobIDs()
    
    (years_of_exp, keywords_list, skipped_jobs) = mainWorkflow(jobIDs)

    # if there were any skipped jobs, try re-doing them
    if (len(skipped_jobs) > 0):
        retry = 5
        time.sleep(2)

        print('Attempting to resolve skipped jobs. Will attempt up to {} times.'.format(retry))
        no_change = 0

        for i in range(retry):
            if (i > 0):
                print('restart!')
            print('iteration {}/{}'.format(i+1, retry))
            time.sleep(0.5)
            last_skipped_count = len(skipped_jobs)
            (skip_years_exp, skip_keywords, skipped_jobs) = mainWorkflow(skipped_jobs)
            if (last_skipped_count == len(skipped_jobs)):
                no_change += 1
                if (no_change >= 2):
                    print("ending retry process at iteration {} since skipped jobs remains at {}.".format(i+1,last_skipped_count))
                    break
            else:
                no_change = 0
            # merge the years-of-experience dictionaries
            for year in skip_years_exp:
                if year in years_of_exp:
                    years_of_exp[year] += skip_years_exp[year]
                else:
                    years_of_exp[year] = skip_years_exp[year]
            keywords_list = keywords_list + skip_keywords
            print('pausing...')
            time.sleep(5)
        
        # final summary
        print('==== final summary (after retry attempts) ====')
        print('Jobs that couldnt be resolved:')
        print(skipped_jobs)
        summarizeResults(years_of_exp, keywords_list)
        

def mainWorkflow(jobIDs):
    'performs the main web scraping workflow and returns the data'
    (years_of_exp, keywords_list, summary_info) = scrapeJobs(jobIDs)

    (data_included, len_data, skipped_jobs) = summary_info
    summarizeResults(years_of_exp, keywords_list, data_included, len_data)

    return (years_of_exp, keywords_list, skipped_jobs)

def scrapeJobs(jobIDs):
    'scrapes the data for the given jobIDs'
    skippedJobs = set()

    years_of_exp = {}
    keywords_list = []

    data_included_count = 0
    step = 0

    for jobID in jobIDs:
        step += 1
        jobData = getJobData(jobID)
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
            print('progress: {}% ({}/{})'.format(round(step/len(jobIDs)*100), step, len(jobIDs)))
    
    summary_info = (data_included_count, len(jobIDs), skippedJobs)
    return (years_of_exp, keywords_list, summary_info)



def getJobIDs():

    timeLimit = 60

    done = False
    i = 0
    jobIDs = set()

    startTime = time.perf_counter()
    print("Getting job IDs")

    while not done:
        #load each page of results, and get all the job IDs from it
        fmtUrl = SEARCH_URL.format(KEYWORD, LOCATION,i)
        print('fetching job IDs from linkedIn at: {}'.format(fmtUrl))
        res = requestURL(fmtUrl)
        # handle for if connection fails for some reason
        if res[0] is False:
            continue
        res = requests.get(fmtUrl)
        soup = BeautifulSoup(res.text, 'html.parser')

        jobDivs = soup.find_all(class_='base-card')

        if (len(jobDivs) == 0):
            done = True
            break

        for div in jobDivs:
            jobID = div.get('data-entity-urn').split(":")[3]
            jobIDs.add(jobID)
        
        i = i + 25 # 25 jobs per results page

    return jobIDs

def getJobData(jobID,debug=False):

    fmtUrl = JOB_URL.format(jobID)
    res = requestURL(fmtUrl)
    # handle for if connection fails for some reason
    if res[0] is False:
        return res
    soup = BeautifulSoup(res[1], 'html.parser')
    
    descriptionSection = soup.find(class_=classNames.description)
    if debug:
        print(descriptionSection)
    if (descriptionSection == None):
        return (False, 'couldnt find description section')
    qualifications = getQualifications2(descriptionSection)

    if qualifications[0] is not False:
        if qualifications[0] >= 10:
            print('High YOE found: {}y [{}]'.format(qualifications[0], jobID))

    return qualifications


def requestURL(url):
    'Try to fetch the URL, and handle if the connection fails'
    try:
        res = requests.get(url, timeout=10)
    except:
        errmsg = 'connection error: Failed to connect to {}'.format(url)
        print(errmsg)
        return (False, errmsg)
    
    return (True, res.text)


def getQualifications2(description):

    # clean the description of unwanted tags that might interfere
    for e in description.findAll('br'):
        e.extract()
    for e in description.findAll('strong'):
        e.extract()

    # first try searching for list tags
    output = searchListTags(description)
    if output[0] is not False:
        return output
    
    # if that fails, try searching for p tags
    output = searchPTags(description)
    if output[0] is not False:
        return output

    return (False, 'No data could be scraped from the description...')

def searchListTags(description):
    'some linkedIn job postings are organized by ul/li tags. this searches in those.'
    keyword_set = set()
    max = 0

    # find the list tags in the description
    ul_tag = description.find('ul')
    if ul_tag == None:
        return (False, 'cant find ul tag')
    all_li = ul_tag.findAll('li')
    if (all_li == None):
        return (False, 'cant find li tags...')

    # check bullet points for tech terms and other useful information
    for li in all_li:
        s = li.string
        if (s == None):
            if (CONFIG.debug_mode):
                print('empty li tag?')
                print(li)
                print('if there are other tags inside <li>, they should be removed.')
            continue

        if (CONFIG.english_only and isForeignScript(s)):
            return (False, 'non-english')

        # 'year' is present, so this line should be listing years experience
        if 'year' in s:
            n = getMaxNumber(s)
            if n > max:
                max = n
        
        # find keywords
        keywords = stripJunk(s)
        keyword_set = keyword_set.union(keywords)
    
    return (max, list(keyword_set))

def searchPTags(description):
    keyword_set = set()
    max = 0

    ptags = description.findAll('p')
    if ptags == None:
        return (False, 'no P tags could be found.')
    
    for p in ptags:
        s = p.nextSibling
        if (s == None) or (type(s) != element.NavigableString):
            if (CONFIG.debug_mode):
                print('empty p tag?')
                print(p)
                print('if there are other tags inside <p>, they should be removed')
            continue
        

        if (CONFIG.english_only and isForeignScript(s)):
            return (False, 'non-english')
        
        # 'year' is present, so this line should be listing years experience
        if 'year' in s:
            n = getMaxNumber(s)
            if n > max:
                max = n
        
        # find keywords
        keywords = stripJunk(s)
        keyword_set = keyword_set.union(keywords)
    
    return (max, list(keyword_set))


def getMaxNumber(s):
    'gets the max number listed in this string'
    tempStr = s.lower()
    max = 0

    stripStr = re.sub('[^0-9]','_', tempStr)
    nums = [n for n in stripStr.split('_') if n != '']
    for n in nums:
        if int(n) > max:
            max = int(n)
    return max
    

# strips all "junk" from an input string and returns the keywords in a set
# expects some form of common language input.
# ex: 
# input ->  "preferred: deep understanding of python, javascript, and mySQL"
# output -> {'python', 'javascript', 'mySQL'}
def stripJunk(s):
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
    tokenized = [word for word in nltk.word_tokenize(s) if not word in ignore] # cut ignore words
    clean1 = [word for word in tokenized if word not in STOP]
    tagged = nltk.pos_tag(clean1)
    nouns = [lemmatizer.lemmatize(word) for (word, pos) in tagged if 'NN' in pos]

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

def removeNonLatinText(s):
    'removes all characters from non-latin scripts (such as Japanese, Arabic, etc)'
    stripStr = re.sub("[^0-9a-zA-Z,.'-]",'_', s) # replaces all non alphanumeric (or not ,.) with _
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

def summarizeResults(years_of_exp, keywords_list, data_included = 0, len_data = 0):
    'shows data gathered from scraping linkedIn, and also displays a summary information of jobs skipped'

    freq_keywords = nltk.FreqDist(keywords_list)
    freq_keywords = [(word, freq) for (word, freq) in freq_keywords.most_common() if freq > CONFIG.keyword_freq]

    print('==== Results ====')
    print('\n')
    print('Frequency of keywords')
    print('\n')
    print(freq_keywords)
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
    print("jobs searched: {}/{} ({}%)".format(data_included,len_data,round(data_included/len_data*100)))
    print("jobs skipped: {}/{}".format(len_data - data_included,len_data))
                


def testJob(jobID):
    jobData = getJobData(jobID,debug=True)
    print(jobData)


jp = '検討・構築。Material-UIをベースとしたUI・TypeScript+React+Next.jsを使用したフロントエンド開発'
en = "We're looking for applicants who are good at handling day-to-day melee in a colisseum; this is fo-real y'all."

#print(stripJunk(jp))

#skiplist = ['3677087147', '3741638968', '3674112838', '3703271863', '3720174333', '3677087669', '3743166474', '3712394524', '3737030771', '3687519020', '3725657486', '3582388673', '3584722414', '3687509515', '3685305343', '3631870943', '3738600072', '3582387238', '3744407826', '3700316017', '3733781008', '3736216642', '3726999350', '3728026973', '3729882785', '3741492739', '3736860595', '3672074548', '3709544257', '3617897187', '3739515829', '3728032821', '3736997633', '3711973405', '3738014531', '3737048454', '3737011236', '3703285703', '3676795165', '3690038965', '3580065537', '3738661646', '3741643989', '3682043208', '3690041761', '3736994785', '3712602139', '3738116530', '3741023293', '3719656213', '3720159226', '3703278062', '3703273802', '3734177380', '3743170124', '3735911450', '3720969496', '3738113702', '3712395056', '3744476673', '3705953361', '3725656466', '3685159482', '3711859854', '3703270649', '3685170888', '3639409053', '3741561283', '3685186078', '3706271614', '3720946338', '3712396900', '3675699453', '3734185629', '3731712277', '3719595157', '3639402900', '3743167459', '3719651344', '3720946474', '3580064945', '3685301425', '3677082030', '3656072268', '3736991976', '3729865655', '3683026965', '3725665233', '3725665732', '3679892254', '3734179400', '3690032572', '3741563167', '3732506229', '3736994845', '3720959984', '3729864973', '3741021556', '3729892619', '3739823489', '3744479208', '3690229169', '3681150260', '3677082882', '3705947881', '3706255829', '3712387638', '3741641931', '3720938889', '3736201254', '3709551056', '3703284548', '3712384492', '3734175146', '3741640820', '3690025577', '3736998250', '3740384810', '3580066983', '3738611463', '3687513261', '3703266277', '3685186788', '3718478302', '3737722007', '3731496702', '3685177044', '3729880128', '3736213949', '3651641535', '3706264771', '3674106846', '3720965676', '3631868997', '3666557862', '3720947816', '3734166985', '3700304062', '3729874021', '3719655964', '3736860538', '3732840780', '3645148380', '3744414589', '3685155060', '3712383426', '3676788939', '3719664606', '3709570260', '3742160774', '3737006698', '3627811808', '3744411463', '3677618495', '3687519102', '3690025572', '3671567979', '3737016432', '3703281573', '3685195617', '3735598695', '3733217412', '3725658588', '3744407719', '3726564902', '3685166670', '3744408256', '3664564121', '3741493697', '3709543102', '3743170276', '3677085464', '3738130552', '3638899945', '3687511244', '3719664764', '3731331688', '3734171694', '3744199202', '3690034015', '3741496594', '3606400560', '3736997890', '3687504614', '3719667931', '3690022868', '3741494568', '3731497733', '3714618130', '3683030483', '3685194920', '3677088581', '3744195755', '3738596699', '3675695761', '3729366069', '3703281188', '3709544008', '3725989757', '3731709227', '3678586035', '3705952214', '3736225370', '3736995869', '3737032058', '3728033132', '3737005176', '3729770652', '3690209841', '3681169022', '3690159216', '3690048569', '3743169258', '3735667829', '3687508184', '3720943832', '3741643700', '3744478451', '3739523299', '3703274676', '3743170132', '3735920144', '3712379163', '3731594717', '3712373966', '3582723326', '3736993871', '3737032389', '3741490920', '3739525432', '3719665522', '3702392092', '3689536005', '3709548922', '3741645237', '3709537898']


#for jobID in skiplist:
#    testJob(jobID)
#    ans = input('enter to continue: ')
#    os.system('clear')

scrapeLinkedIn()