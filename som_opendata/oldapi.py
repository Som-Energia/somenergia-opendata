# coding=utf-8
from dbutils import csvTable
from flask import (
    Blueprint,
    Flask,
    Response,
    make_response,
    )
from functools import wraps
from yamlns import namespace as ns
from consolemsg import u
from .common import (
    yaml_response,
    tsv_response,
    dateSequenceMonths,
    dateSequenceWeeksMonths,
)
from .queries import (
    contractsSeries,
    membersSeries,
)

blueprint = Blueprint(name=__name__, import_name=__name__)

def handle(e, status_code):
    response = make_response(ns(
        error=type(e).__name__,
        message=u(e),
        arguments=e.arguments if hasattr(e,'arguments') else []
        ).dump())
    response.mimetype='application/yaml'
    response.status_code = status_code
    return response


@blueprint.route('/version')
@yaml_response
def version():
    """
    @api {get} /v0.1/version
    @apiVersion 0.1.0
    @apiName Version
    @apiGroup Version
    @apiDescription Response version API

    @apiSampleRequest /{version}/version Version Information
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
    @api {get} /v0.1/contracts/<isodate:fromdate>/monthlyto/<isodate:todate> Contract Data
    @apiVersion 0.1.0
    @apiName Distribution
    @apiGroup Distribution
    @apiDescription Returns a TSV file with the number of contracts for each city and for each date in the interval.
    @apiParam {isodate} fromdate First date in the output
    @apiParam {isodate} todate Last included date in the output, if not specified just fromdate is considered
    @apiSampleRequest /v0.1/contracts/2015-01-01/monthlyto/2015-12-01
    """
    dates=dateSequenceMonths(fromdate, todate)
    filename = 'contracts{frm}{to}.tsv'.format(
        frm = '-'+u(fromdate) if fromdate else '',
        to  = '-'+u(todate) if todate else '',
    )
    return filename, contractsSeries(dates)


@blueprint.route('/members/<isodate:fromdate>')
@blueprint.route('/members/<isodate:fromdate>/monthlyto/<isodate:todate>')
@tsv_response
def members(fromdate=None, todate=None):
    """
    @api {get} /v0.1/members/<isodate:fromdate>[/monthlyto/<isodate:todate>] Members Data
    @apiVersion 0.1.0
    @apiName Distribution
    @apiGroup Distribution
    @apiDescription Returns a TSV file with the number of members for each city and for each date in the interval.
    @apiParam {isodate} fromdate First date in the output
    @apiParam {isodate} todate Last included date in the output, if not specified just fromdate is considered

    @apiSampleRequest /v0.1/members/2015-01-01/monthlyto/2015-12-01
    """
    dates=dateSequenceMonths(fromdate, todate)
    filename = 'contracts{frm}{to}.tsv'.format(
        frm = '-'+u(fromdate) if fromdate else '',
        to  = '-'+u(todate) if todate else '',
    )
    return filename, membersSeries(dates, csvTable)



@blueprint.route('/contracts/<isodate:fromdate>/weeklyandmonthlyto/<isodate:todate>')
@tsv_response
def contractsAux(fromdate=None, todate=None):

    dates=dateSequenceWeeksMonths(fromdate, todate)
    return contractsSeries(dates)


@blueprint.route('/members/<isodate:fromdate>/weeklyandmonthlyto/<isodate:todate>')
@tsv_response
def membersAux(fromdate=None, todate=None):

    dates=dateSequenceWeeksMonths(fromdate, todate)
    return membersSeries(dates, csvTable)





# vim: et sw=4 ts=4
