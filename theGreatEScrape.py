# import the library to parse HTML
from bs4 import BeautifulSoup

# import the library used to query a website
import urllib2
import json

from model import Page, Image, engine
from sqlalchemy.orm import sessionmaker

def crawler(website_url):
    """ find pages on a website """

    try:
        # loop through .tumblr a tags on .tumblr.com, maybe different function with limited number of pages

        # open and read the website
        pageFile = urllib2.urlopen(website_url)
        pageHtml = pageFile.read()
        pageFile.close()

        # call BeautifulSoup on an array of lines in string format
        soup = BeautifulSoup("".join(pageHtml))
        print soup.prettify()[0:1000]

        # find all image sources in array of lines
        pageLinks = soup.findAll("a"]

        for pageLink in pageLinks:
            print pageLink
            # check if item in db, if not - add to db and commit
            possible_page = session.query(Page).filter_by(page_url=pageLink).first()
            if not possible_page:
                page_URL = Page(page_URL=pageLink)
                session.add(page_URL)

        session.commit()

        return page_URL

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

def scrape_image(page_URL):
    """ find all imgsrc on page """

    try:

        # open and read the page
        pageFile = urllib2.urlopen(page_URL)
        pageHtml = pageFile.read()
        pageFile.close()

        # call BeautifulSoup on an array of lines in string format
        soup = BeautifulSoup("".join(pageHtml))
        print soup.prettify()[0:1000]

        # find all image sources in array of lines
        imgsrcs = soup.findAll("img")["src"]

        for imgsrc in imgsrcs:
            print imgsrc
            # check if item in db, if not - add to db and commit
            possible_image = session.query(Image).filter_by(image_url=imgsrc).first()
            if not possible_image:
                src_image = Image(image_url=imgsrc, page_id=page_id)
                session.add(src_image)

        # FIXME: where do i get the page_id? pass through from crawler function, or batches of 100

        session.commit()

        with open("scrape.json", "w") as writeJSON:
            json.dump(scrape, writeJSON)

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

# FIXME scrape text too
# pageURL from crawler function should return a batch of pages, not just one

if __name__ == '__main__':
    page_URL = crawler("https://www.tumblr.com/explore/trending")
    scrape_image()
    Session = sessionmaker(bind=engine)
    session = Session()