""" 
    scrape.py
    
    Defines functions that scrape movie data from various databases
"""

import urllib.request

# IMSDb

uri = "http://www.imsdb.com/all%20scripts/"

f = urllib.request.urlopen(uri)
html = f.read()
f.close()

print(html)

# TODO parse html
# ISSUE scripts are mostly drafts. 
