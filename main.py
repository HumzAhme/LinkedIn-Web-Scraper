from scraper import scrapeLinkedIn, summarizeResults

# main script for running the linkedin web scraper
keywords = scrapeLinkedIn()
summarizeResults(keywords)
