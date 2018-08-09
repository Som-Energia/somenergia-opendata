# -*- coding: utf-8 -*-
import tablib
from dbutils import csvTable
from yamlns import namespace as ns
from .distribution import (
    parse_tsv,
    tuples2objects,
    locationFilter,
    pickDates,
    findTuple,
    includedDates,
    missingDates,
    removeDates,
    includedDatesObject,
    date2field,
    )
from .source import Source
from .missingDataError import MissingDataError
from .missingDateError import MissingDateError

staticColumns = 8

class CsvSource(Source):
    
    data = None

    def __init__(self, content):
        self.data = content
        self._objects = {
            datum : tuples2objects(parse_tsv(data))
            for datum, data in self.data.iteritems()
        }


    def get(self, datum, dates, filters):

        objects = self._objects[datum]

        missing_dates = missingDates(includedDatesObject(objects), dates)
        if missing_dates:
            raise MissingDateError(missing_dates)

        unnecessaryDates = missingDates(dates, includedDatesObject(objects))
        filtered_dates = removeDates(objects, unnecessaryDates)
        filtered_tuples = locationFilter(filtered_dates, filters)

        return filtered_tuples


    def update(self, datum, content):

        _data = tablib.Dataset()
        _data.dict = self._objects[datum]
        _content = tablib.Dataset()
        _content.dict = content
        
        sortedData = _data.sort('codi_ine')
        sortedContent = _content.sort('codi_ine')

        newDates = missingDates(includedDatesObject(_data.dict),
            includedDatesObject(_content.dict)
        )

        for newDate in newDates:
            sortedData.append_col(
                sortedContent[date2field(newDate)],
                header=date2field(newDate)
            )

        self._objects[datum] = [ ns(o)
            for o in sortedData.dict
        ]

