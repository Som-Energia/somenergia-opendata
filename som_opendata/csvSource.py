# -*- coding: utf-8 -*-
import tablib
from dbutils import csvTable
from yamlns import namespace as ns
from .distribution import (
    parse_tsv,
    tuples2objects,
    locationFilter,
    pickDates,
    missedDates,
    findTuple,
    includedDates,
    missingDates,
    removeDates,
    )
from .source import Source
from .missingDataError import MissingDataError
from .missingDateError import MissingDateError

staticColumns = 8

class CsvSource(Source):
    
    data = None

    def __init__(self, content):
        self.data = content
        self._tuples = {
            datum : parse_tsv(data)
            for datum, data in self.data.iteritems()
        }
        self._objects = {
            datum : tuples2objects(_tuples)
            for datum, _tuples in self._tuples.iteritems()
        }


    def get(self, datum, dates, filters):

        tuples = self._tuples[datum]
        objects = self._objects[datum]

        missing_dates = missingDates(includedDates(tuples), dates)
        if missing_dates:
            raise MissingDateError(missing_dates)

        unnecessaryDates = missingDates(dates, includedDates(tuples))
        filtered_dates = removeDates(objects, unnecessaryDates)
        filtered_tuples = locationFilter(filtered_dates, filters)

        return filtered_tuples


    def set(self, datum, content):

        tuples = self._tuples[datum]
        namespaces = self._objects[datum]
        _data = tablib.Dataset()
        _data.dict = namespaces

        _content = tablib.Dataset()
        _content.dict = content
        sortedData = _data.sort('codi_ine')
        sortedContent = _content.sort('codi_ine')
        newHeaders = [
            header
            for header in sortedContent.headers
            if header not in tuples[0]
        ]

        for newHeader in newHeaders:
            sortedData.append_col(
                sortedContent[newHeader],
                header=newHeader
            )
        _datum = sortedData.tsv.replace('\r\n', '\n')


        self.data[datum] = _datum.decode('utf8')[:-1]
        self._tuples[datum] = parse_tsv(self.data[datum])
        self._objects[datum] = tuples2objects(self._tuples[datum])
