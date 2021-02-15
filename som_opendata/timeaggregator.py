# -*- coding: utf-8 -*-
from .common import requestDates

"""
TODO:
- Mover helpers de tiempo a este fichero
- Usar TimeAggregator en
    - api map
    - api data
    - oldapi
"""

class TimeAggregator:
    """
    Time aggregator knows how to aggregate time series
    depending on the metric and the query time params.
    """
    def __init__(self, **kwds):
        self._requestDates = requestDates(**kwds)

    @property
    def requestDates(self):
        "Dates returned after aggregation"
        return self._requestDates

    @property
    def sourceDates(self):
        "Dates required to compute the aggregated metric"
        return self._requestDates

    def aggregate(self, input):
        "Aggregates dates"
        return input



# vim: et sw=4 ts=4
