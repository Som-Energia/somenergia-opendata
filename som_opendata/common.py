import os
from dateutil.relativedelta import relativedelta as delta
from functools import wraps
from yamlns import namespace as ns

from flask import Response, make_response, current_app
from werkzeug.routing import BaseConverter, ValidationError
from yamlns.dateutils import Date
from datetime import date, datetime, timedelta


def getDates(first, last):
    first = Date(first or Date.today())
    return first, Date(last or first)


def dateSequenceMonths(first, last):
    first, last = getDates(first, last)
    interval = delta(last, first)
    months = interval.months + interval.years * 12 + 1
    return [
        first + delta(months=n)
        for n in xrange(0, months)
    ]

def dateSequenceWeeks(first, last):
    first, last = getDates(first, last)
    weeks = (last - first).days / 7 + 1
    return [
        Date(first + delta(weeks=n))
        for n in xrange(0, weeks)
    ]

def dateSequenceYears(first, last):
    first, last = getDates(first, last)
    years = (last - first).days / 365 + 1
    return [
        Date(first + delta(years=n))
        for n in xrange(0, years)
    ]

def requestDates(firstDate, onDate, fromDate, toDate, periodicity):
    return Date.today()


def relative(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


def readQuery(query):
    with open(relative(query + '.sql'), 'r') as queryfile:
        return queryfile.read().rstrip()


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


class IsoCountryA2Converter(BaseConverter):

    def to_python(self, value):
        if (len(value) == 2):
            return str(value)

        raise ValidationError()

    def to_url(self, value):
        if (len(value) == 2):
            return str(value)

        raise ValidationError()


class IsoFrequencyConverte(BaseConverter):

    def to_python(self, value):
        if value == 'weekly' or value == 'monthly' or value == 'yearly':
            return str(value)

        raise ValidationError()

    def to_url(self, value):
        if value == 'weekly' or value == 'monthly' or value == 'yearly':
            return str(value)

        raise ValidationError()


class IsoAggregateLevelConverter(BaseConverter):

    def to_python(self, value):
        if value == 'world' or value == 'countries' or value == 'states' or value == 'ccaas' or value == 'cities':
            return str(value)

        raise ValidationError()

    def to_url(self, value):
        if value == 'world' or value == 'countries' or value == 'states' or value == 'ccaas' or value == 'cities':
            return str(value)

        raise ValidationError()


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
