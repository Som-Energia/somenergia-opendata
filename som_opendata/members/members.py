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


def extractQueryParam(location_filter_req, queryName, objectName):
    queryParam = request.args.getlist(queryName)
    if len(queryParam) != 0:
        location_filter_req[objectName] = queryParam



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
    extractQueryParam(location_filter_req, 'country', 'codi_pais')
    extractQueryParam(location_filter_req, 'ccaa', 'codi_ccaa')
    extractQueryParam(location_filter_req, 'state', 'codi_provincia')
    extractQueryParam(location_filter_req, 'city', 'codi_ine')

    filtered_objects = locationFilter(objects, location_filter_req)

    if len(filtered_objects) > 0: return aggregate(filtered_objects, al)
    else: return ns()


members_modul.source = None