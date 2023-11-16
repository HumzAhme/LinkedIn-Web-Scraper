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
