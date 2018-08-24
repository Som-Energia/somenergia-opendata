# -*- encoding: utf-8 -*-
from flask import Flask, current_app
from .oldapi import blueprint as oldapi
from .csvSource import loadCsvSource
from .printer import api
from .common import (
    register_handlers,
    register_converters,
    )


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
