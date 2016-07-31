"""Models and database functions for web scraper."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Page(db.Model):
    """Pages to be scraped."""

    __tablename__ = "pages"

    page_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    page_URL = db.Column(db.String(255), nullable=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'))

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

    return "<Page page_id=%s page_URL=%s>" % (self.page_id, self.page_URL)


class Image(db.Model):
    """Images to be scraped."""

    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image_URL = db.Column(db.String(255), nullable=True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.page_id'))

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

    return "<Image image_id=%s image_URL=%s>" % (self.image_id, self.image_URL)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pages'
    db.app = app
    db.init_app(app)

# https://cloud.google.com/vision/


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."