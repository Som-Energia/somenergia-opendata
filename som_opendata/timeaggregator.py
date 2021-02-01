# -*- coding: utf-8 -*-
from .common import requestDates

class TimeAggregator:
    """
    Time aggregator knows how to aggregate time series
    depending on the metric and the query time params.
    """
    def __init__(self, **kwds):
        self.outputDates = requestDates(**kwds)


# vim: et sw=4 ts=4
