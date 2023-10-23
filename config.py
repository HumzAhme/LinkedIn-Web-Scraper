class config:
    # allow only english content to be searched?
    english_only = False
    # debug mode enables showing detailed output of possible errors in the search
    debug_mode = True
    # frequency cut off for keywords - only keywords of this frequency or above will appear in results
    keyword_freq = 3
    # set to enable pausing to occur in the script; mostly when summaries are displayed for an end user
    enable_pausing = True
    # set to enable logging misc updates to the console; mostly for status updates on the progress of the app
    enable_misc_logging = True

class debugger:
    # find the string producing a certain term - script pauses to show you which string produced a certain term
    find_terms = False
    # words in this set will be paused on if find_terms is on
    find_list = {'s','j','sw','t','ci','pl','k','d','m','cd','pl'}

