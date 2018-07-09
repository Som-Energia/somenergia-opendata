
from flask import (
    Blueprint,
    Flask,
    make_response,
    Response,
    json,
    )

import logging
from yamlns import namespace as ns
from functools import wraps
import os
import psycopg2
import dbconfig as config
from dbutils import csvTable
from common import yaml_response
from socis.socis import modul_socis


VERSION = 4



old_modul = Blueprint(name='old_modul', import_name=__name__)

sentry = None

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


from yamlns.dateutils import Date

from .common import (
    dateSequence,
    readQuery,
    )

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


def activeMembersCounter(adate):
    # TODO: Unsafe substitution
    return """
    count(CASE
        WHEN create_date IS NULL THEN NULL
        WHEN create_date > '{adate}'::date THEN NULL
        WHEN data_baixa_soci < '{adate}'::date THEN NULL
        WHEN create_date <= '{adate}'::date THEN TRUE
            WHEN active THEN TRUE
        ELSE NULL
            END) AS count_{adate:%Y_%m_%d}
        """.format(adate=adate)



def membersSparse(dates, dbhandler, debug=False):
    #adate = dates[0]

    db = psycopg2.connect(**config.psycopg)
    query = readQuery('members_distribution')
    query = query.format(','.join(
        activeMembersCounter(Date(adate))
        for adate in dates
        ))
    with db.cursor() as cursor :
        cursor.execute(query)
        return csvTable(cursor)



    query = query.format(Date(adate),Date(adate),Date(adate))
    with db.cursor() as cursor :
        cursor.execute(query)
        return csvTable(cursor)


"""
@api {get} /old/version
@apiVersion 1.0.1
@apiName Version
@apiGroup Version
@apiDescription Response version API

@apiSampleRequest http://DNS-NAME:5001/old/version
@apiSuccessExample {yaml} Success-Response:
    HTTP/1.1 200OK
    {
        version: 1.0
    }
"""


@old_modul.route('/version')
@yaml_response
def version():
    return ns(
        version = '1.0',
        )


"""
@api {get} /old/contracts/<isodate:fromdate>/monthlyto/<isodate:todate>
@apiVersion 1.0.1
@apiName Contracts
@apiGroup Contracts
@apiDescription Retorna un fitxer yaml amb els contractes de cada pais-ccaa-provincia-municipi


@apiSampleRequest http://DNS-NAME:5001/old/contracts/2015-01-01/monthlyto/2015-12-01
@apiSuccessExample {yaml} Success-Response:
    HTTP/1.1 200OK
    {
        dates: 
            - 2018-01-01
            level: countries
            countries:
              ES:
                name: Espanya
                data: [2020]
                ccaas:
                  '09':
                    name: Catalunya
                    data: [2020]
                    states:
                      '17':
                        name: Girona
                        data: [2020]
    }
"""


@old_modul.route('/contracts/<isodate:fromdate>')
@old_modul.route('/contracts/<isodate:fromdate>/monthlyto/<isodate:todate>')
@tsv_response
def contracts(fromdate=None, todate=None):
    dates=dateSequence(fromdate, todate)
    return contractsSeries(dates)


"""
@api {get} /old/members/<isodate:fromdate>/monthlyto/<isodate:todate>
@apiVersion 1.0.1
@apiName Members
@apiGroup Members
@apiDescription Retorna un fitxer yaml amb els socis de cada pais-ccaa-provincia-municipi


@apiSampleRequest http://DNS-NAME:5001/old/members/2015-01-01/monthlyto/2015-12-01
@apiSuccessExample {yaml} Success-Response:
    HTTP/1.1 200OK
    {
        dates: 
            - 2018-01-01
            level: countries
            countries:
              ES:
                name: Espanya
                data: [2020]
                ccaas:
                  '09':
                    name: Catalunya
                    data: [2020]
                    states:
                      '17':
                        name: Girona
                        data: [2020]
    }
"""

@old_modul.route('/members/<isodate:fromdate>')
@old_modul.route('/members/<isodate:fromdate>/monthlyto/<isodate:todate>')
@tsv_response
def members(fromdate=None, todate=None):
    dates=dateSequence(fromdate, todate)
    return membersSparse(dates, csvTable)
