"""Models and database functions for web scraper."""

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, \
    create_engine, Sequence
from sqlalchemy.ext.declarative import \
    declarative_base
from sqlalchemy.orm import relationship


DB_URI = "postgresql:///scrapes"

Base = declarative_base()


##############################################################################
""" Model definition """

class Page(Base):
    """Pages to be scraped."""

    __tablename__ = "pages"

    page_id = Column(Integer(), autoincrement=True, primary_key=True)
    page_URL = Column(String(255), nullable=True)

    # define relationship to image
    # images = relationship("Image",
    #                        primaryjoin="and_(Page.page_id==Image.page_id)",
    #                        backref="page")


    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<Page page_id=%s page_URL=%s>" % (self.page_id, self.page_URL)


class Image(Base):
    """Images to be scraped."""

    __tablename__ = "images"

    image_id = Column(Integer(), autoincrement=True, primary_key=True)
    image_URL = Column(String(255), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<Image image_id=%s image_URL=%s>" % (self.image_id, self.image_URL)


class PageImageLink(Base):
    """Association table connecting pages to images."""

    __tablename__ = "page_image_link"

    page_id = Column(Integer(), ForeignKey('pages.page_id'), primary_key=True, autoincrement='ignore_fk')
    image_id = Column(Integer, ForeignKey('images.image_id'), primary_key=True, autoincrement='ignore_fk')


    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<PageImageLink page_id=%s image_id=%s>" % (self.page_id, self.image_id)


##############################################################################
""" Create tables if not already created, and connect to python API"""

engine = create_engine(DB_URI, echo=True)

Base.metadata.create_all(engine)


# https://cloud.google.com/vision/
# create table for text
