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
    )
from .source import Source
from .missingDataError import MissingDataError

staticColumns = 8

class CsvSource(Source):
    
    data = None

    def __init__(self, content):
        self.data = content


    # TODO: Refactor --> "1 sol raise"
    def get(self, datum, dates, filters):

        tuples = parse_tsv(self.data[datum])

        if not tuples:
            raise MissingDataError([], dates, None)

        filtered_dates = pickDates(tuples, dates)

        if not filtered_dates or len(filtered_dates[0]) < staticColumns + len(dates):
            raise MissingDataError(locationFilter(tuples2objects(filtered_dates), filters), missedDates(tuples, dates), None)

        objectList = tuples2objects(filtered_dates)
        filtered_tuples = locationFilter(objectList, filters)
        if not filtered_tuples:
            raise MissingDataError(filtered_tuples, None, None)

        return filtered_tuples


    def set(self, datum, content):

        tuples = parse_tsv(self.data[datum])
        namespaces = tuples2objects(tuples)
        _data = tablib.Dataset()
        _data.dict = namespaces

        _content = tablib.Dataset()
        _content.dict = content
        sortedData = _data.sort('codi_ine')
        sortedContent = _content.sort('codi_ine')
        newHeaders = [header
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
