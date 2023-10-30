class config:
    # keyword to include in the job search URL
    keywords = ['Software Developer','Software Engineer']
    # location to include in the job search URL
    location = None
    # allow only english content to be searched?
    english_only = False
    # debug mode enables the debug config and showing detailed output of possible errors in the search
    # this should be turned off when other code is listening for output
    debug_mode = True
    # frequency cut off for keywords - only keywords of this frequency or above will appear in results
    keyword_freq = 5
    # set to enable pausing to occur in the script; mostly when summaries are displayed for an end user
    enable_pausing = True
    # set to enable logging misc updates to the console; mostly for status updates on the progress of the app
    # this should be turned off when other code is listening for output
    enable_misc_logging = True
    # minimum number of jobs to be searched; if the finding jobs step doesn't find enough, it retries
    min_job_count = 1000
    # number of times the code can retry loading data for skipped jobs
    retry_count = 10

class debugger:
    # find the string producing a certain term - script pauses to show you which string produced a certain term
    find_terms = False
    # words in this set will be paused on if find_terms is on
    find_list = {''}

