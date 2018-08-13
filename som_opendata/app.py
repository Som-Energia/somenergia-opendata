# -*- encoding: utf-8 -*-
import dbconfig as config
import logging
import os.path
import records
from flask import Flask, current_app
from yamlns import namespace as ns
from .api import old_modul
from .printer.printer import printer_module
from som_opendata.common import (
    handle_bad_request,
    handle_request_not_found,
    IsoAggregateLevelConverter,
    IsoCountryA2Converter,
    IsoDateConverter,
    IsoFrequencyConverte,
    IsoFieldConverter,
    )


VERSION = 4
sentry = None

# TODO: TEST READCSVFILES
def readCsvFiles():
    myPath = os.path.abspath(os.path.dirname('.'))
    datums = ns()
    for datum, path in config.opendata.iteritems():
        with open(myPath + path) as f:
            csvFile = f.read()
        datums[datum] = csvFile
    return datums

def init_db():
    current_app.csvData = readCsvFiles()

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

    app.url_map.converters['isodate'] = IsoDateConverter
    app.url_map.converters['country'] = IsoCountryA2Converter
    app.url_map.converters['frequency'] = IsoFrequencyConverte
    app.url_map.converters['aggregateLevel'] = IsoAggregateLevelConverter
    app.url_map.converters['field'] = IsoFieldConverter

    app.register_blueprint(old_modul, url_prefix='/old')
    app.register_blueprint(printer_module, url_prefix='/printer')
    app.register_error_handler(404, handle_request_not_found)
    app.register_error_handler(400, handle_bad_request)

    with app.app_context():
        init_db()
        current_app.errors = None

    return app


#if __name__ == '__main__':
app = create_app()

# vim: et ts=4 sw=4
