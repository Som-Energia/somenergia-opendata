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
    )    
from ..distribution import (
    parse_tsv,
    tuples2objects,
    aggregate,
    locationFilter,
    pickDates,
    )


members_modul = Blueprint(name='members_modul', import_name=__name__)


def validateInputDates(ondate = None, since = None, todate = None):
    return not (not ondate is None and (not since is None or not todate is None))



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

    relation_locationLevel_id = [
            ['country', 'codi_pais'],
            ['ccaa', 'codi_ccaa'],
            ['state', 'codi_provincia'],
            ['city', 'codi_ine']
          ]

    for locationLevel_id in relation_locationLevel_id:
        extractQueryParam(location_filter_req, *locationLevel_id)

    filtered_objects = locationFilter(objects, location_filter_req)

    if len(filtered_objects) > 0: return aggregate(filtered_objects, al)
    else: return ns()


members_modul.source = None