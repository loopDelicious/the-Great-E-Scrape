# import the library to parse HTML
from bs4 import BeautifulSoup

# import the library used to query a website
import urllib2

from model import connect_to_db, db, Page, Image


try:
    # open and read the website
    pageFile = urllib2.urlopen("http://candiceswanepoeldaily.tumblr.com/")
    pageHtml = pageFile.read()
    pageFile.close()

    # call BeautifulSoup on an array of lines in string format
    soup = BeautifulSoup("".join(pageHtml))

    # find all links in array of lines
    hrefs = soup.findAll("a")

    for href in hrefs:
        print href

    # check if item in db, if not - add to db and commit

except urllib2.URLError as e:
    # exception handling for URLError
    if hasattr(e, 'reason'):
        print "We failed to reach a server."
        print "Reason: ", e.reason
    # exception handling for HTTPError
    elif hasattr(e, 'code'):
        print 'The server couldn\'t fulfill the request.'
        print 'Error code; ', e.code
    else:
        print 'Everything is fine.'