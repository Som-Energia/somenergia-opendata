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


    # TODO: Refactor --> "1 sol raise"
    def get(self, datum, dates, filters):

        tuples = self._tuples[datum]

        if not tuples:
            raise MissingDateError(dates)

        filtered_dates = pickDates(tuples, dates)

        if not filtered_dates:
            raise MissingDateError(
                missedDates(tuples, dates)
                )

        if len(filtered_dates[0]) < staticColumns + len(dates):
            raise MissingDateError(
                missedDates(tuples, dates)
                )

        objectList = tuples2objects(filtered_dates)
        filtered_tuples = locationFilter(objectList, filters)

        return filtered_tuples



    def set(self, datum, content):

        tuples = self._tuples[datum]
        namespaces = tuples2objects(tuples)
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
