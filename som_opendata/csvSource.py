# -*- coding: utf-8 -*-
import tablib
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
    field2date,
    getDates,
    isField,
    )
from .errors import MissingDateError
from future.utils import iteritems


class CsvSource(object):
    
    data = None

    def __init__(self, content):
        self.data = content
        self._objects = {
            datum : tuples2objects(parse_tsv(data))
            for datum, data in iteritems(self.data)
        }

    # TODO: Change name datum -> metric
    def getLastDay(self, datum):
        d = parse_tsv(self.data[datum])
        return field2date(d[0][len(d[0])-1])

    def get(self, datum, dates, filters):

        objects = self._objects[datum]
        missing_dates = missingDates(includedDatesObject(objects), dates)
        if missing_dates:
            raise MissingDateError(missing_dates)

        filtered_tuples = locationFilter(objects, filters)
        if len(dates) < self.countLength / 2:
            requested_dates = getDates(filtered_tuples, dates)
        else:
            unnecessaryDates = missingDates(dates, includedDatesObject(objects))
            requested_dates = removeDates(filtered_tuples, unnecessaryDates)

        return requested_dates


    def update(self, datum, content):

        _data = tablib.Dataset()
        _data.dict = self._objects[datum]
        _content = tablib.Dataset()
        _content.dict = content
        
        addObjects(self._objects[datum], content)

import dbconfig as config
import os.path
import glob

def loadCsvSource(relativePath='../data'):
    myPath = os.path.abspath(os.path.dirname(__file__))
    dataPath = os.path.join(myPath, relativePath)
    datums = ns()
    for datafile in glob.glob(os.path.join(dataPath,'*.tsv')):
        datum = os.path.splitext(os.path.basename(datafile))[0]
        with open(datafile) as f:
            csvFile = f.read()
        datums[datum] = csvFile
    return CsvSource(datums)


