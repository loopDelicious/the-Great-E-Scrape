"""
    scraper to find all job postings in San Francisco
"""
from bs4 import BeautifulSoup
import urllib2


def scrape_jobs(page):
    """ find all job postings on page """

    try:

        # open and read the page
        pageFile = urllib2.urlopen(page)
        pageHtml = pageFile.read()
        pageFile.close()

        # call BeautifulSoup on an array of lines in string format
        soup = BeautifulSoup("".join(pageHtml), "html.parser")
        # print soup.prettify()[0:1000]

        # find all San Francisco jobs in array of lines
        # pageLinks = soup.findAll("a", {"href": True})

        for link in soup.find_all('a', {'href': True}):
            if soup.p.string == "San Francisco":
                print(link.get('href'))

        # import pdb; pdb.set_trace()
        # return jobs

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

    # create a configured Session class
    # Session = sessionmaker(bind=engine)
    # # create a Session
    # session = Session()

    jobs = scrape_jobs("https://www.womenwhocode.com/jobs")

    # print jobs

