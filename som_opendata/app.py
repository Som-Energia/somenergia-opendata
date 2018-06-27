import logging

from flask import Flask, current_app
from socis.socis import modul_socis
from api import old_modul
import records
import dbconfig as config
from som_opendata.common import IsoDateConverter, IsoCountryA2Converter, handle_request_not_found, handle_bad_request

VERSION = 4
sentry = None


def init_db():
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

    app.register_blueprint(old_modul, url_prefix='/old')
    app.register_blueprint(modul_socis, url_prefix='/socis')
    app.register_error_handler(404, handle_request_not_found)
    app.register_error_handler(400, handle_bad_request)
    app.teardown_appcontext

    with app.app_context():
        init_db()
        current_app.errors = None

    return app


app = create_app()
