from bs4 import BeautifulSoup

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