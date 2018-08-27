# -*- encoding: utf-8 -*-
import os
from dateutil.relativedelta import relativedelta as delta
from datetime import date
from flask import Response, make_response, current_app, jsonify
from functools import wraps
from werkzeug.routing import BaseConverter, ValidationError
from yamlns.dateutils import Date
from yamlns import namespace as ns
from .missingDateError import MissingDateError



def getDates(first, last):
    first = Date(first or Date.today())
    return first, Date(last or first)


def dateSequenceMonths(first, last):
    first, last = getDates(first, last)
    interval = delta(last, first)
    months = interval.months + interval.years * 12 + 1
    return [
        first + delta(months=n)
        for n in range(0, months)
    ]

def dateSequenceWeeks(first, last):
    first, last = getDates(first, last)
    weeks = (last - first).days / 7 + 1
    return [
        Date(first + delta(weeks=n))
        for n in range(0, weeks)
    ]

def dateSequenceYears(first, last):
    first, last = getDates(first, last)
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


def requestDates(first=None, on=None, since=None, to=None, periodicity=None):

    if periodicity:
        request_date = ((since or first), (to or Date.today()))
        frequency_method = caseFrequency(periodicity)
        all_dates = frequency_method(*request_date)

    elif on: all_dates = dateSequenceWeeks(on, on)

    else: all_dates = dateSequenceWeeks(Date.today(), Date.today())

    return [str(date) for date in all_dates]


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

class IsoFrequencyConverte(BaseConverter):

    def to_python(self, value):
        if value == 'monthly' or value == 'yearly':
            return str(value)

        raise ValidationError('Incorrect Frequency')

    def to_url(self, value):
        if value == 'monthly' or value == 'yearly':
            return str(value)

        raise ValidationError()


class IsoAggregateLevelConverter(BaseConverter):

    def to_python(self, value):
        if value == 'world' or value == 'country' or value == 'state' or value == 'ccaa' or value == 'city':
            return str(value)

        raise ValidationError('Incorrect Aggregate Level')

    def to_url(self, value):
        if value == 'world' or value == 'country' or value == 'state' or value == 'ccaa' or value == 'city':
            return str(value)

        raise ValidationError()

class IsoFieldConverter(BaseConverter):

    def to_python(self, value):
        if value == 'members' or value == 'contracts':
            return value    
        raise ValidationError('Incorrect Frequency')

    def to_url(self, value):
        if value == 'members' or value == 'contracts':
            return value
        raise ValidationError()

def register_converters(app):
    app.url_map.converters['isodate'] = IsoDateConverter
    app.url_map.converters['frequency'] = IsoFrequencyConverte
    app.url_map.converters['geolevel'] = IsoAggregateLevelConverter
    app.url_map.converters['field'] = IsoFieldConverter


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
def handle_missingDateError(error):
    return make_response(
        jsonify(ns(message=error.description, errorId=error.errorId)),
        error.code
    )

def register_handlers(app):
    app.register_error_handler(404, handle_request_not_found)
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(MissingDateError, handle_missingDateError)


