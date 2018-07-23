# -*- coding: utf-8 -*-
from functools import wraps
from flask import Blueprint, request, current_app, abort
from yamlns import namespace as ns
from yamlns.dateutils import Date
from ..common import (
        yaml_response,
        dateSequenceMonths,
        dateSequenceWeeks,
        dateSequenceYears,
        requestDates,
        pickDates,
    )    
from ..data import (
    ExtractData,
    )
from ..datafromcsv import DataFromCSV
from ..distribution import (
    parse_tsv,
    tuples2objects,
    aggregate,
    locationFilter,
    )


members_modul = Blueprint(name='members_modul', import_name=__name__)



@members_modul.route('')
@members_modul.route('/on/<isodate:ondate>')
@members_modul.route('/by/<aggregateLevel:al>')
@members_modul.route('/by/<aggregateLevel:al>/on/<isodate:ondate>')
@members_modul.route('/by/<aggregateLevel:al>/<frequency:frequency>')
@members_modul.route('/by/<aggregateLevel:al>/<frequency:frequency>/from/<isodate:fromdate>')
@members_modul.route('/by/<aggregateLevel:al>/<frequency:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@members_modul.route('/by/<aggregateLevel:al>/<frequency:frequency>/to/<isodate:todate>')
@members_modul.route('/<frequency:frequency>')
@members_modul.route('/<frequency:frequency>/from/<isodate:fromdate>')
@members_modul.route('/<frequency:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@members_modul.route('/<frequency:frequency>/to/<isodate:todate>')
@yaml_response
def members(al='world', ondate=None, frequency=None, fromdate=None, todate=None):
    content = members_modul.source
    tuples = parse_tsv(content)
    request_dates = requestDates(first=members_modul.firstDate, on=ondate, since=fromdate, to=todate, periodicity=frequency)
    filtered_tuples = pickDates(tuples, request_dates)
    objects = tuples2objects(filtered_tuples)

    location_filter_req = ns()
    country = request.args.getlist('country')
    if len(country) != 0:
        location_filter_req['country'] = country
    state = request.args.getlist('state')
    if len(state) != 0:
        location_filter_req['state'] = state
    ccaa = request.args.getlist('ccaa')
    if len(ccaa) != 0:
        location_filter_req['ccaa'] = ccaa
    city = request.args.getlist('city')
    if len(city) != 0:
        location_filter_req['city'] = city


    # location_filter_req = ns(country=country, ccaa=ccaa, state=state, city=city)

    filtered_objects = locationFilter(objects, location_filter_req)

    result = aggregate(filtered_objects, al)
    return result



    # Actualment default és que dongui del primer al final
    date = ondate or ((fromdate or '2010-01-01'), (todate or Date.today()))
    frequency_method = caseFrequency(frequency)
    dates = caseDates(date)
    d = frequency_method(dates[0], dates[1])
    dCorrect = [str(dat) for dat in d]

    data = ExtractData().extractObjects('members', dCorrect, DataFromCSV())

    data = tuples2objects(data)


    return aggregate(data, al)


members_modul.source = None