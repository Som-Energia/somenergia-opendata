    #!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    Flask,
    make_response,
    Response,
    )

import logging
from yamlns import namespace as ns
from functools import wraps
import os
import psycopg2
import dbconfig as config
from dbutils import csvTable

app = Flask(__name__)


sentry = None

if app.config.get('SENTRY_DSN', False):
    from raven.contrib.flask import Sentry
    sentry = Sentry(app)
    sentry.client.tags_context({'version': VERSION})

def sentry_exception():
    if not sentry: return
    sentry.client.captureException()

def handle(e, status_code):
    response = make_response(ns(
        error=type(e).__name__,
        message=str(e),
        arguments=e.arguments if hasattr(e,'arguments') else []
        ).dump())
    response.mimetype='application/yaml'
    response.status_code = status_code
    return response


def yaml_response(f):
    @wraps(f)
    def wrapper(*args, **kwd):
        result = f(*args, **kwd)

        if type(result) is Response:
            return result

        response = make_response(ns(result).dump())
        response.mimetype='application/yaml'
        return response
    return wrapper

def utf8(thing):
    if type(thing) is unicode: return thing
    if type(thing) is str: return unicode(thing,'utf-8',errors='ignore')
    return unicode(thing)

def tsv_response(f):
    @wraps(f)
    def wrapper(*args, **kwd):
        result = f(*args, **kwd)

        if type(result) is Response:
            return result
        if type(result) in (str,unicode):
            response = make_response(result)
            response.mimetype='text/tab-separated-values'
            response.headers["Content-Disposition"] = "filename=contracts.tsv"
            return response

        response = make_response('\n'.join(
            '\t'.join(
                utf8(x)
                    .replace('\t',' ')
                    .replace('\n',' ')
                for x in line)
            for line in result
        ))
        response.mimetype='text/tab-separated-values'
        response.charset='utf-8'
        response.headers["Content-Disposition"] = "attachment; filename=myplot.tsv"
        return response
    return wrapper


# isodate converter

from werkzeug.routing import BaseConverter
from yamlns.dateutils import Date
class IsoDateConverter(BaseConverter):

    def to_python(self, value):
        return Date(value)

    def to_url(self, value):
        return str(value)


app.url_map.converters['isodate'] = IsoDateConverter

@app.route('/version')
@yaml_response
def version():
    return ns(
        version = '1.0',
        )

from dateutil.relativedelta import relativedelta as delta
def dateSequence(first, last):
    first = Date(first or Date.today())
    last = Date(last or first)
    return [
        first + delta(months=n)
        for n in xrange(0, delta(last,first).months+1)
        ]

def relative(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__),path))


def readQuery(query):
    with open(relative(query+".sql"), 'r') as queryfile:
        return queryfile.read().rstrip()

def contractsSparse(dates):
    db = psycopg2.connect(**config.psycopg)
    query = readQuery('contract_distribution_sparse')
    with db.cursor() as cursor :
        cursor.execute(query, dict(dates=[
            [Date(adate) for adate in dates]
        ]))
        return csvTable(cursor)

def contractsSeries(dates):
    db = psycopg2.connect(**config.psycopg)
    query = readQuery('contract_distribution')
    query = query.format(','.join(
        activeContractCounter(Date(adate))
        for adate in dates
        ))
    with db.cursor() as cursor :
        cursor.execute(query)
        return csvTable(cursor)


@app.route('/contracts/<isodate:fromdate>')
@app.route('/contracts/<isodate:fromdate>/monthlyto/<isodate:todate>')
@tsv_response
def contracts(fromdate=None, todate=None):
    dates=dateSequence(fromdate, todate)
    return contractsSeries(dates)

@app.route('/members/<isodate:fromdate>')
@tsv_response
def members(fromdate=None):
    db = psycopg2.connect(**config.psycopg)
    with db.cursor() as cursor :
        cursor.execute(open(relative("distribucio_de_socies.sql"),"r").read().rstrip(), dict(
        date=fromdate,
        ))

        return csvTable(cursor)

def activeContractCounter(adate):
    # TODO: Unsafe substitution
    return """
	count(CASE
		WHEN polissa.data_alta IS NULL THEN NULL
		WHEN polissa.data_alta > '{adate}'::date THEN NULL
		WHEN polissa.data_baixa is NULL then TRUE
		WHEN polissa.data_baixa > '{adate}'::date THEN TRUE
		ELSE NULL
		END) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def activeContractLister(adate):
    # TODO: Unsafe substitution
    return """
	string_agg(CASE
		WHEN polissa.data_alta IS NULL THEN NULL
		WHEN polissa.data_alta > '{adate}'::date THEN NULL
		WHEN polissa.data_baixa is NULL then polissa.id::text
		WHEN polissa.data_baixa > '{adate)s'::date THEN polissa.id::text
		ELSE NULL
		END, ',' ORDER BY polissa.id) AS ids_{adate},
""".format(adate=adate)


# vim: et ts=4 sw=4
