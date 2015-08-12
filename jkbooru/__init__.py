# -*- coding: utf-8 -*-
import os
import hashlib
from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from jkbooru.config.default_config import DefaultConfig

app = Flask(__name__)
app.config.from_object(DefaultConfig)
db = SQLAlchemy(app)
from jkbooru.model.post import Post


@app.route('/', defaults={'page': 1})
@app.route('/post/<int:page>')
def index(page):
    return 'Hello World!' + str(page)


@app.route('/detail/<int:post_id>')
def detail(post_id):
    return 'Hello World!'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file is not None:
            filename_ext = secure_filename(file.filename).rsplit('.', 1)
            filename = filename_ext[0].encode('utf-8')
            filename = hashlib.sha224(filename).hexdigest()
            filename += '.' + filename_ext[1]
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            post = Post(filename=filename)
            db.session.add(post)
            db.session.commit()
            return 'uploaded'
    elif request.method == 'GET':
        return 'get'
