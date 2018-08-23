#!/usr/bin/env python
import sys
from som_opendata.app import app


if __name__ == '__main__':
    context = None
    if app.config.get('USE_SSL', False):
        context = app.config['SSL_CERT'], app.config['SSL_KEY']

    try:
        app.run(
    #        host=app.config.get('IP', '127.0.0.1'),
            host=app.config.get('IP', '0.0.0.0'),
            port=app.config.get('PORT', 5001),
            ssl_context=context,
            debug=app.config.get('DEBUG', False) or '--debug' in sys.argv,
        )
    except (KeyboardInterrupt, SystemExit):
        db_conn = getattr(app, 'db', None)
        if db_conn is not None:
            db_conn.close()
