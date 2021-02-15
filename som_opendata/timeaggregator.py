# -*- coding: utf-8 -*-
from yamlns.dateutils import Date as isoDate
from .common import requestDates
import datetime

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
        self._periodicity = kwds.get('periodicity')

    @property
    def requestDates(self):
        "Dates returned after aggregation"
        return self._requestDates

    @property
    def sourceDates(self):
        "Dates required to compute the aggregated metric"
        return self._requestDates

    def aggregate(self, input):
        "Aggregates data by dates"
        return input

    @staticmethod
    def Create(operator, **kwds):
        cls = _timeAggregatorClasses.get(operator, TimeAggregator)
        return cls(**kwds)


class TimeAggregatorSum(TimeAggregator):
    """
    Time aggregator for Sum operations.
    """
    @property
    def sourceDates(self):
        "Dates required to compute the aggregated metric"
        if self._periodicity != 'yearly':
            return self._requestDates
        return sum((
            fullYear(date)
            for date in self._requestDates
        ),[])


    def aggregate(self, input):
        "Aggregates data by dates"
        if self._periodicity != 'yearly':
            return input
        return [
            sum(input[start:end])
            for start, end in zip(
                range(0, len(input), 12),
                range(12, len(input)+1, 12),
            )
        ]


def fullYear(isodate):
    """
    Given the first of january returns a list of 12
    first of months including january itself.
    """
    date = isoDate(isodate)
    return [
        str(isoDate(date.year-1, month, 1))
        for month in range(2,13)
    ] + [isodate]


_timeAggregatorClasses = dict(
    last = TimeAggregator,
    sum = TimeAggregatorSum,
)



# vim: et sw=4 ts=4
