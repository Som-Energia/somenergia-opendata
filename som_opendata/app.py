# -*- encoding: utf-8 -*-
import dbconfig as config
import logging
import os.path
from flask import Flask, current_app
from yamlns import namespace as ns
from .oldapi import blueprint as oldapi
from csvSource import CsvSource
from .printer.printer import api
from som_opendata.common import (
    register_handlers,
    register_converters,
    )


VERSION = 4

def loadCsvSource():
    myPath = os.path.abspath(os.path.dirname('.'))
    datums = ns()
    for datum, path in config.opendata.iteritems():
        with open(os.path.join(myPath, path)) as f:
            csvFile = f.read()
        datums[datum] = csvFile
    return CsvSource(datums)



def create_app():
    app = Flask(__name__)

    register_converters(app)
    register_handlers(app)

    app.register_blueprint(oldapi, url_prefix='/v0.1')
    app.register_blueprint(api, url_prefix='/v0.2')

    api.source = loadCsvSource()

    app.errors = None

    return app


app = create_app()

# vim: et ts=4 sw=4
