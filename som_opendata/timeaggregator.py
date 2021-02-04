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
        self.requestDates = requestDates(**kwds)
        self.sourceDates = self.requestDates[:]

    def aggregate(self, input):
        return input

# vim: et sw=4 ts=4
