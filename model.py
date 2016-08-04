"""Models and database functions for web scraper."""

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, \
    create_engine, Sequence
from sqlalchemy.ext.declarative import \
    declarative_base
from sqlalchemy.orm import sessionmaker



DB_URI = "postgresql:///scrapes"

Base = declarative_base()


##############################################################################
""" Model definition """

class Page(Base):
    """Pages to be scraped."""

    __tablename__ = "pages"

    page_id = Column(Integer(), Sequence('user_id_seq'), primary_key=True)
    page_URL = Column(String(255), nullable=True)
    image_id = Column(Integer(), ForeignKey('images.image_id'))

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<Page page_id=%s page_URL=%s>" % (self.page_id, self.page_URL)


class Image(Base):
    """Images to be scraped."""

    __tablename__ = "images"

    image_id = Column(Integer(), Sequence('user_id_seq'), primary_key=True)
    image_URL = Column(String(255), nullable=True)
    page_id = Column(Integer(), ForeignKey('pages.page_id'))

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<Image image_id=%s image_URL=%s>" % (self.image_id, self.image_URL)


##############################################################################
""" Create tables if not already created, and connect to python API"""

engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


# https://cloud.google.com/vision/
