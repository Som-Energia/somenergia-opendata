#!/usr/bin/env python
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    from som_opendata.api import app, sentry, logging
    context = None
    if app.config.get('USE_SSL',False):
        context = app.config['SSL_CERT'], app.config['SSL_KEY']

    if app.config.get('SENTRY_DSN', False):
        sentry.client.captureMessage(
            "Starting API-WEBFORMS...",
            level=logging.INFO)

    import sys
    app.run(
#        host=app.config.get('IP', '127.0.0.1'),
        host=app.config.get('IP', '0.0.0.0'),
        port=app.config.get('PORT', 5001),
        ssl_context=context,
        debug=app.config.get('DEBUG', False) or  '--debug' in sys.argv,
        )


# vim: et ts=4 sw=4
