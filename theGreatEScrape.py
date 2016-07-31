# import the library to parse HTML
from bs4 import BeautifulSoup

# import the library used to query a website
import urllib2

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