# import the library to parse HTML
from bs4 import BeautifulSoup

# import the library used to query a website
import urllib2
import json

from model import Page, Image, engine
from sqlalchemy.orm import sessionmaker

def scrapey():
    """ find URL and all imgsrc on page """

    try:

        # loop through .tumblr a tags on .tumblr.com, maybe different function with limited number of pages

        # open and read the website
        pageFile = urllib2.urlopen("http://candiceswanepoeldaily.tumblr.com/")
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
        # https://www.tumblr.com/explore/trending - scrape text, images

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

if __name__ == '__main__':

    scrapey()
    Session = sessionmaker(bind=engine)
    session = Session()