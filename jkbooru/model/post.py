# -*- coding: utf-8 -*-
from jkbooru import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True)

    def __init__(self, filename):
        self.filename = filename

    def __repr__(self):
        return '<Post %r>' % self.path
