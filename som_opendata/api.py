    #!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    abort,
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    Response,
    session,
    )

import logging

app = Flask(__name__)


sentry = None

if app.config.get('SENTRY_DSN', False):
    from raven.contrib.flask import Sentry
    sentry = Sentry(app)
    sentry.client.tags_context({'version': VERSION})

def sentry_exception():
    if not sentry: return
    sentry.client.captureException()


@app.route('/version')
def version():
    return jsonify(
        version = '1.0',
        )



# vim: et ts=4 sw=4
