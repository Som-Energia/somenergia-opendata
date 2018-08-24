# coding=utf-8
import dbconfig as config
import psycopg2
from dbutils import csvTable
from flask import (
    Blueprint,
    Flask,
    Response,
    make_response,
    )
from functools import wraps
from yamlns import namespace as ns
from .common import yaml_response


VERSION = 4



blueprint = Blueprint(name=__name__, import_name=__name__)

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
    if type(thing) is str: return thing
    if type(thing) is str: return str(thing,'utf-8',errors='ignore')
    return str(thing)

def tsv_response(f):
    @wraps(f)
    def wrapper(*args, **kwd):
        result = f(*args, **kwd)

        if type(result) is Response:
            return result
        if type(result) in (str,str):
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
    dateSequenceMonths,
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
    db = psycopg2.connect(**config.psycopg)
    query = readQuery('members_distribution')
    query = query.format(','.join(
        activeMembersCounter(Date(adate))
        for adate in dates
        ))
    with db.cursor() as cursor :
        cursor.execute(query)
        return csvTable(cursor)



@blueprint.route('/version')
@yaml_response
def version():
    """
    @api {get} /v0.1/version
    @apiVersion 0.1.0
    @apiName Version
    @apiGroup Version
    @apiDescription Response version API

    @apiSampleRequest /{version}/version
    @apiSuccessExample {yaml} Success-Response:
        HTTP/1.1 200OK
        version: 0.1.0
        compat: 0.1.0
    """
    return ns(
        version = '0.1.0',
        compat = '0.1.0',
        )


@blueprint.route('/contracts/<isodate:fromdate>')
@blueprint.route('/contracts/<isodate:fromdate>/monthlyto/<isodate:todate>')
@tsv_response
def contracts(fromdate=None, todate=None):
    """
    @api {get} /v0.1/contracts/<isodate:fromdate>/monthlyto/<isodate:todate>
    @apiVersion 0.1.0
    @apiName Distribution
    @apiGroup Distribution
    @apiDescription Returns a TSV file with the number of contracts for each city and for each date in the interval.
    @apiParam {isodate} fromdate First date in the output
    @apiParam {isodate} todate Last included date in the output, if not specified just fromdate is considered
    @apiSampleRequest /v0.1/contracts/2015-01-01/monthlyto/2015-12-01
    """
    dates=dateSequenceMonths(fromdate, todate)
    return contractsSeries(dates)


@blueprint.route('/members/<isodate:fromdate>')
@blueprint.route('/members/<isodate:fromdate>/monthlyto/<isodate:todate>')
@tsv_response
def members(fromdate=None, todate=None):
    """
    @api {get} /v0.1/members/<isodate:fromdate>[/monthlyto/<isodate:todate>]
    @apiVersion 0.1.0
    @apiName Distribution
    @apiGroup Distribution
    @apiDescription Returns a TSV file with the number of members for each city and for each date in the interval.
    @apiParam {isodate} fromdate First date in the output
    @apiParam {isodate} todate Last included date in the output, if not specified just fromdate is considered

    @apiSampleRequest /v0.1/members/2015-01-01/monthlyto/2015-12-01
    """
    dates=dateSequenceMonths(fromdate, todate)
    return membersSparse(dates, csvTable)


# vim: et sw=4 ts=4
