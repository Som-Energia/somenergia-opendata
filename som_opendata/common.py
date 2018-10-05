# -*- encoding: utf-8 -*-
import os
from dateutil.relativedelta import relativedelta as delta
from datetime import date, timedelta
from flask import Response, make_response, current_app, jsonify
from functools import wraps
from werkzeug.routing import BaseConverter, ValidationError
from yamlns.dateutils import Date
from yamlns import namespace as ns
from .errors import (
    MissingDateError,
    ValidateError,
)


def previousFirstOfMonth(date):
    return str(Date(date).replace(day=1))

def getDates(first, last):
    first = Date(first or Date.today())
    return first, Date(last or first)


def dateSequenceMonths(first, last):
    first, last = getDates(first, last)
    if first.day != 1:
        first = first.replace(day=1)
    interval = delta(last, first)
    months = interval.months + interval.years * 12 + 1
    return [
        first + delta(months=n)
        for n in range(0, months)
    ]

def dateSequenceWeeks(first, last):
    first, last = getDates(first, last)
    if first.isoweekday() != 1:
        first = Date(first - timedelta(days=first.isoweekday()-1%7))
    weeks = (last - first).days / 7 + 1
    return [
        Date(first + delta(weeks=n))
        for n in range(0, weeks)
    ]

def dateSequenceWeeksMonths(first, last):
    m = dateSequenceMonths(first, last)
    w = dateSequenceWeeks(first, last)
    return set(m + w)



def dateSequenceYears(first, last):
    first, last = getDates(first, last)
    if first.day != 1 or first.month != 1:
        first = first.replace(day=1, month=1)
    years = (last - first).days / 365 + 1
    return [
        Date(first + delta(years=n))
        for n in range(0, years)
    ]

def caseFrequency(frequency):
    if frequency == 'weekly':
        return dateSequenceWeeks
    elif frequency == 'monthly':
        return dateSequenceMonths
    else:
        return dateSequenceYears


def requestDates(first=None, last=None, on=None, since=None, to=None, periodicity=None):
    """
    Returns a list of dates to be requested given the query parameters.
    @param periodicity: 'weekly', 'monthly', 'yearly' or None if single date
    @param first: First date in available history
    @param last: Last date in available history
    @param on: Single date to be retrieved or none if 
    @param since: Earlier date to be retrieved or none if first
    @param to: Later date to be retrieved or none if last
    """
    if periodicity:
        since = since or first
        to = to or last or str(Date.today())
        all_dates = caseFrequency(periodicity)(since, to)
        return [str(date) for date in all_dates]

    if on:
        return [previousFirstOfMonth(on)]

    return [last or str(Date.today())]



def relative(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


def readQuery(query):
    with open(relative(query + '.sql'), 'r') as queryfile:
        return queryfile.read().rstrip()

def utf8(thing):
    if type(thing) is unicode: return thing
    if type(thing) is str: return unicode(thing,'utf-8',errors='ignore')
    return str(thing)

def tsv_response(f):
    @wraps(f)
    def wrapper(*args, **kwd):
        filename, result = f(*args, **kwd)

        if type(result) is Response:
            return result
        if type(result) in (str,str):
            response = make_response(result)
            response.mimetype='text/tab-separated-values'
            response.headers["Content-Disposition"] = "filename={}".format(filename or 'file.tsv')
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


def yaml_response(f):
    @wraps(f)
    def wrapper(*args, **kwd):
        result = f(*args, **kwd)

        if type(result) is Response:
            return result

        response = make_response(ns(result).dump())
        response.mimetype = 'application/yaml'
        return response
    return wrapper


class IsoDateConverter(BaseConverter):

    def to_python(self, value):
        return Date(value)

    def to_url(self, value):
        return str(value)


# None i world son valors por defecto de los parametros
valorsAptes = ns(metric=['members', 'contracts'],
        frequency=['monthly', 'yearly', None],
        geolevel=['country', 'ccaa', 'state', 'city', 'world']
        )

def validateParams(field, value):
    if value not in valorsAptes[field]:
        raise ValidateError(field, value)

def register_converters(app):
    app.url_map.converters['isodate'] = IsoDateConverter

@yaml_response
def handle_request_not_found(e):
    response = make_response('Request not found!', 404)
    response.mimetype = 'application/yaml'
    return response


@yaml_response
def handle_bad_request(self):
    if current_app.errors == None:
        response =  make_response('Bad Request', 400)
    else:
        response = make_response(
            '\'{}\' no existeix/en'.format(', '.join([str(x) for x in current_app.errors])), 400
        )
        current_app.errors = None
    response.mimetype = 'application/yaml'
    return response

@yaml_response
def handle_customErrorValidation(error):
    return make_response(
        jsonify(ns(message=error.description,
            metric=error.metric,
            valueRequest=error.value,
            possibleValues=error.possibleValues
            )), error.code
    )

@yaml_response
def handle_missingDatesError(error):
    return make_response(
        jsonify(ns(message=error.description)), error.code
    )

def register_handlers(app):
    app.register_error_handler(404, handle_request_not_found)
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(MissingDateError, handle_missingDatesError)
    app.register_error_handler(ValidateError, handle_customErrorValidation)


def enable_cors(app):
    # In production and testing servers, CORS is managed by the server,
    # Call this just for development server
    from flask_cors import CORS
    CORS(app, resources={
        r'/*': dict(
            origins = '*',
            supports_credentials = True, # Send cookies, requires no '*' origin
            send_wildcard = False, # So, instead of '*' copy 'Origin' from request header
        )})



# vim: et ts=4 sw=4
