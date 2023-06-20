from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class RequestCount(db.Model):
    __tablename__ = "request_counts"

    count = db.Column(db.Integer, nullable=False)
    cluster = db.Column(db.String(100), primary_key=True)
    tick = db.Column(db.DateTime, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
