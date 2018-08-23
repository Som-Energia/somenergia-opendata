# -*- encoding: utf-8 -*-
import dbconfig as config
import logging
import os.path
import records
from flask import Flask, current_app
from yamlns import namespace as ns
from .api import blueprint as oldapi
from csvSource import CsvSource
from .printer.printer import printer_module
from som_opendata.common import (
    handle_bad_request,
    handle_request_not_found,
    handle_missingDateError,
    register_converters,
    )
from som_opendata.missingDateError import MissingDateError


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

def init_db():
    current_app.csvData = readCsvFiles()
    current_app.csvSource = CsvSource(current_app.csvData)

    current_app.db = records.Database(
        'postgres://{user}:{password}@{host}:{port}/{database}'.format(**config.psycopg)
    )


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

    app.register_blueprint(oldapi, url_prefix='')
    #app.register_blueprint(printer_module, url_prefix='')
    app.register_error_handler(404, handle_request_not_found)
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(MissingDateError, handle_missingDateError)

    with app.app_context():
        init_db()
        current_app.errors = None

    return app


app = create_app()

# vim: et ts=4 sw=4
