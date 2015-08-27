from werkzeug import secure_filename
from flask.ext.script import Command, Option
from jkbooru import app, db
from jkbooru.model.post import Post


class CrawlCommand(Command):
    def get_options(self):
        return [
            Option('-s', '--server', dest='server', default='yande.re'),
            Option('-t', '--tags', dest='tags', default='wallpaper'),
        ]

    def run(self, server, tags):
        import http.client
        import urllib
        import json
        import os
        import hashlib

        conn = http.client.HTTPSConnection(server)
        for i in range(1, 50):
            conn.request("GET", "/post.json?page=" + str(i)
                                + "&tags=" + urllib.parse.unquote(tags))
            res = conn.getresponse()
            if res.status is 200:
                data = json.loads(res.read().decode())
                for item in data:
                    file_url = item['file_url']
                    print(file_url)
                    filename_ext = secure_filename(file_url).rsplit('.', 1)
                    filename = hashlib.sha224(filename_ext[0].encode('utf-8'))
                    filename = filename.hexdigest() + '.' + filename_ext[1]

                    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    # urllib.request.urlretrieve(file_url, path)
                    os.system('wget -O ' + path + ' ' + file_url)

                    post = Post(filename=filename)
                    db.session.add(post)
                    db.session.commit()
            else:
                print("Error ( Status: " + res.status + ", Reason: "
                                                        + res.reason)
        return
