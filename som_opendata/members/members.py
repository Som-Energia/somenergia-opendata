# -*- coding: utf-8 -*-
from functools import wraps
from flask import Blueprint, request, current_app, abort
from yamlns import namespace as ns

from ..common import yaml_response




members_modul = Blueprint(name='members_modul', import_name=__name__)

@members_modul.route('/by/<aggregateLevel:al>')
@members_modul.route('/by/<aggregateLevel:al>/on/<isodate:ondate>')
@members_modul.route('/by/<aggregateLevel:al>/<frequency:frequency>')
@members_modul.route('/by/<aggregateLevel:al>/<frequency:frequency>/from/<isodate:fromdate>')
@members_modul.route('/by/<aggregateLevel:al>/<frequency:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@members_modul.route('/by/<aggregateLevel:al>/<frequency:frequency>/to/<isodate:todate>')
# @tsv_response
# def members(fromdate=None, todate=None):
#     dates=dateSequenceMonths(fromdate, todate)
#     return membersSparse(dates, csvTable)



