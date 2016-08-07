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
        soup = BeautifulSoup("".join(pageHtml), "html.parser")
        # print soup.prettify()[0:1000]

        # find all links with hashtag cat, limit to 100 results
        # FIXME add hashtag cat requirement (string = "#cat")
        pageLinks = soup.findAll("a", {"href": True}, limit=100)
        # import pdb; pdb.set_trace()
        page_URLs = []

        for pageLink in pageLinks:
            pageLink = pageLink['href']

            # if URL does not have a domain, add the main page's domain'
            if pageLink[0] == '/' and pageLink[:1] != '//':
                pageLink = website_url + pageLink

            # check if item in db, if not - add to db and commit
            existing_page = session.query(Page).filter_by(page_URL=pageLink).first()

            # add to array of link strings
            page_URLs.append(pageLink)

            if not existing_page:
                page_URL = Page(page_URL=pageLink)
                session.add(page_URL)
                session.commit()

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
        soup = BeautifulSoup("".join(pageHtml), "html.parser")
        # print soup.prettify()[0:1000]

        # find all image sources in array of lines
        imgs = soup.findAll("img")

        for img in imgs:

            # check if item in db under this page, if not - add to db and commit
            page_id = session.query(Page).filter_by(page_URL=page_URL).first()
            existing_image = session.query(Image).filter_by(image_URL=img["src"]).first()

            if not existing_image:
                src_image = Image(image_URL=img["src"])
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

    # create a configured Session class
    Session = sessionmaker(bind=engine)
    # create a Session
    session = Session()

    page_URLs = crawler("https://www.tumblr.com/explore/trending")

    for page_URL in page_URLs:
        scrape_image(page_URL)

