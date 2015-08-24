# -*- coding: utf-8 -*-
import os
import hashlib
from flask import Flask, request, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from jkbooru.config.default_config import DefaultConfig

app = Flask(__name__)
app.config.from_object(DefaultConfig)
db = SQLAlchemy(app)
from jkbooru.model.post import Post


@app.route('/', defaults={'page_idx': 1})
@app.route('/posts/<int:page_idx>')
def index(page_idx):
    pagination = Post.query.paginate(page_idx, per_page=15, error_out=False)
    return render_template('page.html', settings={
        'title': app.config['JKBOORU_TITLE'],
        'description': app.config['JKBOORU_DESCRIPTION']
    }, page={
        'next': pagination.next_num,
        'prev': pagination.prev_num,
        'current': pagination.page,
        'total': pagination.pages,
        'per_page': pagination.per_page,
        'posts': pagination.items
    })


@app.route('/detail/<int:post_id>')
def detail(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    return render_template('detail.html', settings={
        'title': app.config['JKBOORU_TITLE'],
        'description': app.config['JKBOORU_DESCRIPTION']
    }, post=post)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file is not None:
            filename_ext = secure_filename(file.filename).rsplit('.', 1)
            filename = hashlib.sha224(filename_ext[0].encode('utf-8'))
            filename = filename.hexdigest() + '.' + filename_ext[1]

            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            post = Post(filename=filename)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('detail', post_id=post.id))
    elif request.method == 'GET':
        return render_template('upload.html', settings={
            'title': app.config['JKBOORU_TITLE'],
            'description': app.config['JKBOORU_DESCRIPTION']
        })
