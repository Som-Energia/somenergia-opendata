import os
from dateutil.relativedelta import relativedelta as delta
from functools import wraps
from yamlns import namespace as ns

from flask import Response, make_response, current_app
from werkzeug.routing import BaseConverter, ValidationError
from yamlns.dateutils import Date


def dateSequence(first, last):
    first = Date(first or Date.today())
    last = Date(last or first)
    interval = delta(last, first)
    months = interval.months + interval.years * 12 + 1
    return [
        first + delta(months=n)
        for n in xrange(0, months)
    ]


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


@yaml_response
def handle_request_not_found(e):
    response = make_response('Request not found!', 404)
    response.mimetype = 'application/yaml'
    return response
