from scraper import scrapeLinkedIn, summarizeResults
from upload import upload_json
from config import config

# main script for running the linkedin web scraper
(keywords, filename) = scrapeLinkedIn()
summarizeResults(keywords)
if config.upload_cloud:
    upload_json('{}.json'.format(filename))