# -*- encoding: utf-8 -*-
from flask import Flask
from .csvSource import loadCsvSource
from .api import api
from .common import (
    register_handlers,
    register_converters,
    enable_cors,
    )
from .templateSource import loadMapData
from .tsvRelativeMetricSource import loadTsvRelativeMetric
from .local_groups import loadYamlLocalGroups
from flask_babel import Babel
from flask import request


def create_app():
    app = Flask(__name__)

    register_converters(app)
    register_handlers(app)
    enable_cors(app) # TODO: Config whether to call it, server may handle it
    app.register_blueprint(api, url_prefix='/v0.2')
    api.localGroups = loadYamlLocalGroups()
    api.source = loadCsvSource(aliases=dict(localgroup=api.localGroups.data))
    api.mapTemplateSource = loadMapData()
    api.relativeMetricSource = loadTsvRelativeMetric()
    api.firstDate = '2010-01-01'
    app.errors = None
    app.config['LANGUAGES'] = ['en', 'es', 'ca', 'eu', 'gl']
    babel = Babel()
    babel.init_app(app)
    for rule in app.url_map.iter_rules():
        print(rule)

    @babel.localeselector
    def get_locale():
        lang = request.args.get('lang')
        if lang in app.config['LANGUAGES']:
            return lang
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    return app


app = create_app()

# vim: et ts=4 sw=4
