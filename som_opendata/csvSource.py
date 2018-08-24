# -*- coding: utf-8 -*-
import tablib
from dbutils import csvTable
from yamlns import namespace as ns
from .distribution import (
    parse_tsv,
    tuples2objects,
    locationFilter,
    includedDates,
    missingDates,
    removeDates,
    includedDatesObject,
    date2field,
    addObjects,
    )
from .missingDateError import MissingDateError


class CsvSource():
    
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
        
        addObjects(self._objects[datum], content)

import dbconfig as config
import os.path

def loadCsvSource():
    myPath = os.path.abspath(os.path.dirname(__file__))
    datums = ns()
    for datum, path in config.opendata.iteritems():
        with open(os.path.join(myPath, path)) as f:
            csvFile = f.read()
        datums[datum] = csvFile
    return CsvSource(datums)


