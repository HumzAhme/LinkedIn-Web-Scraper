# LinkedIn-Web-Scraper
Gets the keywords and tech terms currently popular in LinkedIn job postings for Software Developer jobs

## Required Setup
This python project uses pipenv to contain its package dependencies. So first, make sure pipenv is set up and dependencies installed:
```
pipenv install
```
The dependencies it installs are listed in Pipfile. If any errors occur while installing, take a look in there and make sure things like the Python version are compatible with
what you have. You should be able to change the Python version as long as its Python3.

## Config
You will want to look through config.py to make sure configuration options match your intentions.
If you aren't Ben, you won't have the credentials (or at least you shouldn't...) to upload data to the cloud storage bucket, so you'll wanna at least set:
```python
upload_cloud: False
```
The other config options have descriptions provided, so look around and change what you like.  A lot of them are just used by me while debugging during development.

## How to run
The main workflow is contained in main.py.  You'll be running this file to execute the search algorithm and have the output printed to your screen / saved to a JSON.
Execute it this way from the terminal:
```
pipenv run python3 main.py
```
If you decide to branch this for your own development, you may also like using test.py for testing purposes. It has a large set of test IDs to speed up testing.
In general, to run any file using the pipenv:
```
pipenv run python3 <filename.py>
```

## Data Output
If a run succeeds, the output should be saved to /projectFolder/data/currentDate.json

(projectFolder would be the folder containing the python scripts)

The JSON will be formatted as follows:

```python
[
  searchedJobCount,
  [
    "word",
    freq
  ],
  ...
]
```

the first item of the array, searchedJobCount, will be an integer telling you how many jobs were searched in total.
Each item in the array following is a word data array, where the first item is the word string, and the second is the number of jobs it appeared in.
From there, you can calculate the percentage each word appears by dividing freq with searchedJobCount to get the relative frequency it appears in job descriptions.

Note: even if a word appears more than once in a given job description, its frequency count is only incremented by 1.

## Google cloud storage
If you're interested in accessing the full to-date dataset of monthly data, let me know and I can help you access the google cloud storage bucket.
