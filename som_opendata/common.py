# -*- encoding: utf-8 -*-

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

def caseFrequency(frequency):
    if frequency == 'weekly':
        return dateSequenceWeeks
    elif frequency == 'monthly':
        return dateSequenceMonths
    else:
        return dateSequenceYears


def requestDates(first, on, since, to, periodicity):

    if periodicity:
        request_date = ((since or first), (to or Date.today()))
        frequency_method = caseFrequency(periodicity)
        all_dates = frequency_method(*request_date)

    elif on: all_dates = dateSequenceWeeks(on, on)

    else: all_dates = dateSequenceWeeks(Date.today(), Date.today())

    return [str(date) for date in all_dates]


def eliminateIrrelevantDates(dataWithDates, dates):

    pass
    '''
    headersPerEliminar = [
        index for index, value in enumerate(dataWithDates[0])
        if 'count' in value and not any([value == 'count_'+date.replace('-','_') for date in dates])
    ]

    return [
        [element for index, element in enumerate(l) if index not in headersPerEliminar]
        for l in dataWithDates
    ]
    '''

def pickDates(tuples, dates):

    return [
            ['codi_pais', 'pais', 'codi_ccaa', 'comunitat_autonoma', 'codi_provincia', 'provincia', 'codi_ine', 'municipi', 'count_2018_01_01'],
            ['ES', 'España', '09', 'Catalunya', '17', 'Girona', '17007', 'Amer', '2000']
           ]
    '''
    dataImportant = eliminateIrrelevantDates(tuples, dates)

    if len(dataImportant[0]) <= 8:
        return []
    else:
        return dataImportant
    '''



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
