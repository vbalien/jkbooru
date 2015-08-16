#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.script import Command, Manager
from flask.ext.migrate import Migrate, MigrateCommand
from jkbooru import app, db

migrate = Migrate(app, db)
manager = Manager(app)


class Debug(Command):
    def run(self):
        app.run(host='0.0.0.0', port=80, debug=True)


class Run(Command):
    def run(self):
        app.run(host='0.0.0.0', port=80, debug=False)

manager.add_command('debug', Debug)
manager.add_command('run', Run)
manager.add_command('db', MigrateCommand)
manager.run()
