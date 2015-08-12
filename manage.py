#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.script import Command, Manager
from jkbooru import app

manager = Manager(app)


class Debug(Command):
    def run(self):
        print("run")
        app.run(host='0.0.0.0', port=80, debug=True)


class Run(Command):
    def run(self):
        app.run(host='0.0.0.0', port=80, debug=False)

manager.add_command('debug', Debug)
manager.add_command('run', Run)
manager.run()
