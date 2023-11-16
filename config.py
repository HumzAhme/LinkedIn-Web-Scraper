class config:
    # keyword to include in the job search URL
    keywords = ['Software Developer','Software Engineer', 'Backend Engineer', 'Frontend Engineer', 'Fullstack Engineer']
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
    # number of times the code can retry loading data for skipped jobs
    retry_count = 10
    # set to enable saving results to google cloud
    upload_cloud = True
    # set if you are doing a full test run. shortens the search process by limiting the number of jobs it searches.
    # also adds a "test" suffix to the json's filename so real data isn't accidentally overwritten on google cloud.
    # mostly for a quick test that nothing in the process crashes or has obvious errors
    test_run = False
    # threshold for allowing data into the results. represents the percentage of jobs a term appears in.
    freq_threshold = 0.005

class debugger:
    # find the string producing a certain term - script pauses to show you which string produced a certain term
    find_terms = True
    # words in this set will be paused on if find_terms is on
    find_list = {'ass', 'b', 'container', 'rail'}

