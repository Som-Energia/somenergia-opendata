# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app, make_response, send_file, jsonify
from yamlns import namespace as ns
from .common import (
    yaml_response,
    optional_json,
    svg_response,
    optional_tsv,
    validateParams,
    validateMapParams,
)
from .timeaggregator import TimeAggregator
from . import common
from .distribution import getAggregated, aggregated2table
from .errors import MissingDateError
from . import __version__
from .map import renderMap
from flask_babel import Babel, get_locale


api = Blueprint(name=__name__.split('.')[-1], import_name=__name__, template_folder='../')
api.firstDate = '2010-01-01'


@api.route('/version')
@yaml_response
@optional_json
def version():
    return ns(
        version = __version__,
        compat = '0.2.1',
        )

@api.route('/spec')
@yaml_response
def spec():
    if 'json' in request.args.getlist('format'):
        response = jsonify(ns.load('./openapi.yaml'))
        print(response)
        response.headers['Content-Disposition'] ='attachment; filename=somenergia-opendata-{}.json'.format(__version__)
        return response
    return send_file(
        '../openapi.yaml',
        mimetype = 'application/yaml',
        as_attachment = True,
        attachment_filename = "somenergia-opendata-{}.yaml".format(__version__),
    )


@api.route('/discover/metrics')
@yaml_response
@optional_json
def discoverMetrics():
    return ns(metrics=[
        ns(
            id = key,
            text = format(value.text), # Translates
            description = format(value.description), # Translates
        )
        for key,value in common.metrics.items()
    ])


@api.route('/discover/geolevel')
@yaml_response
@optional_json
def discoverGeoLevel():
    return ns(
        geolevels = [
        ns(data,
            id=key,
            text=format(data.text), # overwrite lazy translated
        )
        for key, data in common.geolevels.items()
    ])

@api.route('/discover/geolevel/<geolevel>')
@yaml_response
@optional_json
def discoverGeoLevelOptions(geolevel):
    filters = locationFiltersFromQuery()
    return ns(options=api.source.geolevelOptions(geolevel, **filters))

def locationFiltersFromQuery():
    """Extracts any relevant query parameter to build a filter.
    """
    return ns(
        (key, request.args.getlist(key))
        for key in [
            # TODO: take list from source
            'country',
            'ccaa',
            'state',
            'city',
            'localgroup',
        ]
        if key in request.args
    )

def validateInputDates(ondate = None, since = None, todate = None):
    return ondate is None or (
        since is None and todate is None
    )


@api.route('/<string:metric>') # TODO: UNTESTED
@api.route('/<string:metric>/on/<isodate:ondate>')
@api.route('/<string:metric>/<string:frequency>')
@api.route('/<string:metric>/<string:frequency>/from/<isodate:fromdate>')
@api.route('/<string:metric>/<string:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@api.route('/<string:metric>/<string:frequency>/to/<isodate:todate>')
@api.route('/<string:metric>/by/<string:geolevel>')
@api.route('/<string:metric>/by/<string:geolevel>/on/<isodate:ondate>')
@api.route('/<string:metric>/by/<string:geolevel>/<string:frequency>')
@api.route('/<string:metric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>')
@api.route('/<string:metric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@api.route('/<string:metric>/by/<string:geolevel>/<string:frequency>/to/<isodate:todate>')
@yaml_response
@optional_json
@optional_tsv(tabulator=aggregated2table)
def distribution(metric=None, geolevel='world', ondate=None, frequency=None, fromdate=None, todate=None):

    validateParams(
        frequency=frequency,
        metric=metric,
        geolevel=geolevel,
    )

    timeDomain = TimeAggregator.Create(
        operator = common.metrics[metric].timeaggregation,
        first=api.firstDate,
        last=api.source.getLastDay(metric),
        on=ondate,
        since=fromdate,
        to=todate,
        periodicity=frequency,
    )

    filters = locationFiltersFromQuery()

    return getAggregated(
        source=api.source,
        metric=metric,
        timeDomain=timeDomain,
        location_filter=filters,
        geolevel=geolevel,
        mutable=False,
    )


@api.route('/map/<string:metric>')
@api.route('/map/<string:metric>/on/<isodate:ondate>')
@api.route('/map/<string:metric>/by/<string:geolevel>')
@api.route('/map/<string:metric>/by/<string:geolevel>/on/<isodate:ondate>')
@api.route('/map/<string:metric>/by/<string:geolevel>/<string:frequency>')
@api.route('/map/<string:metric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@api.route('/map/<string:metric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>')
@api.route('/map/<string:metric>/by/<string:geolevel>/<string:frequency>/to/<isodate:todate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/on/<isodate:ondate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/on/<isodate:ondate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/<string:frequency>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/<string:frequency>/to/<isodate:todate>')
@svg_response
def map(metric=None, ondate=None, geolevel='ccaa', frequency=None, fromdate=None, todate=None, relativemetric=None):

    validateMapParams(
        frequency=frequency,
        geolevel=geolevel,
        metric=metric,
        relativemetric=relativemetric,
    )

    timeDomain = TimeAggregator.Create(
        operator = common.metrics[metric].timeaggregation,
        first=api.firstDate,
        last=api.source.getLastDay(metric),
        on=ondate,
        since=fromdate,
        to=todate,
        periodicity=frequency,
    )

    filters = locationFiltersFromQuery()
    locationCodes = api.relativeMetricSource.getCodesByGeolevel(geolevel=geolevel)
    #locationCodes = api.source.geolevelOptions(geolevel, **filters).keys()
    relativeMValues = api.relativeMetricSource.getValuesByCode(
        metric=relativemetric,
        geolevel=geolevel,
    ) if relativemetric else dict()

    template=api.mapTemplateSource.getTemplate(
        geolevel=geolevel,
        lang=str(get_locale()),
        filters=filters,
    )
    result = renderMap(
        source=api.source,
        metric=metric,
        timeDomain=timeDomain,
        geolevel=geolevel,
        template=template,
        legendTemplate=api.mapTemplateSource.getLegend(),
        locationsCodes=locationCodes,
        relativeMetricValues=relativeMValues,
        filters=filters,
    )
    response = make_response(result)
    response.mimetype = 'image/svg+xml'
    return response

api.source = None
api.mapTemplateSource = None
api.relativeMetricSource = None
api.localGroups = None



# vim: et ts=4 sw=4
