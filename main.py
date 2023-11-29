from scraper import scrapeLinkedIn, summarizeResults
from googlecloud import upload_json
from config import config

# main script for running the linkedin web scraper
(keywords, filename) = scrapeLinkedIn()
summarizeResults(keywords[1:]) # first index is the job count
if config.upload_cloud:
    upload_json(filename)