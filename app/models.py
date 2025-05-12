from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Page(db.Model):

    __tablename__ = "pages"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True, nullable=False)
    header_found = db.Column(db.Boolean, default=False)
    footer_found = db.Column(db.Boolean, default=False)
    header_selector = db.Column(db.String(255))
    footer_selector = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_media = db.Column(db.Boolean, default=False)
    links = db.Column(db.JSON)
    title = db.Column(db.Text)
    meta_description = db.Column(db.Text)
    content = db.Column(db.Text)
    image_urls = db.Column(db.JSON)
    published_date = db.Column(db.DateTime)
