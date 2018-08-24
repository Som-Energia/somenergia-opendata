# -*- encoding: utf-8 -*-
import dbconfig as config
import logging
import os.path
import records
from flask import Flask, current_app
from yamlns import namespace as ns
from .oldapi import blueprint as oldapi
from csvSource import CsvSource
from .printer.printer import printer_module
from som_opendata.common import (
    register_handlers,
    register_converters,
    )


VERSION = 4
sentry = None

def readCsvFiles():
    myPath = os.path.abspath(os.path.dirname('.'))
    datums = ns()
    for datum, path in config.opendata.iteritems():
        with open(os.path.join(myPath, path)) as f:
            csvFile = f.read()
        datums[datum] = csvFile
    return datums



def create_app():
    app = Flask(__name__)

    if app.config.get('SENTRY_DSN', False):
        from raven.contrib.flask import Sentry
        sentry = Sentry(app)
        sentry.client.tags_context({'version': VERSION})
        sentry.client.captureMessage(
            "Starting API-WEBFORMS...",
            level=logging.INFO
        )

    register_converters(app)
    register_handlers(app)

    app.register_blueprint(oldapi, url_prefix='/v0.1')
    app.register_blueprint(printer_module, url_prefix='/v0.2')

    app.csvData = readCsvFiles()
    app.csvSource = CsvSource(app.csvData)

    app.db = records.Database(
        'postgres://{user}:{password}@{host}:{port}/{database}'.format(**config.psycopg)
    )
    app.errors = None

    return app


app = create_app()

# vim: et ts=4 sw=4
