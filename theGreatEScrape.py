""" crawler function to find all links on page with specified criteria
    scrape_image function to find all images on each linked to page
"""
from bs4 import BeautifulSoup
import urllib2

import json

from model import Page, Image, PageImageLink, engine
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

        # find all links with hashtag cat, limit to 100 results
        # FIXME add hashtag cat requirement (string = "#cat")
        pageLinks = soup.findAll("a", limit=100)
        # import pdb; pdb.set_trace()
        page_URLs = []

        for pageLink in pageLinks:
            print pageLink
            # check if item in db, if not - add to db and commit
            possible_page = session.query(Page).filter_by(page_url=pageLink).first()
            if not possible_page:
                page_URL = Page(page_URL=pageLink)
                session.add(page_URL)
                session.commit()
                page_URLs.append(page_URL)
        # import pdb; pdb.set_trace()
        return page_URLs

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
            # check if item in db under this page, if not - add to db and commit
            page_id = session.query(Page).filter_by(page_URL=page_URL).first()
            possible_image = session.query(Image).filter_by(image_url=imgsrc, page_id=page_id).first()

            if not possible_image:
                src_image = Image(image_url=imgsrc)
                session.add(src_image)
                session.commit()

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

if __name__ == '__main__':

    page_URLs = crawler("https://www.reddit.com/")

    for page_URL in page_URLs:
        scrape_image(page_URL)

    # create a configured Session class
    Session = sessionmaker(bind=engine)
    # create a Session
    session = Session()