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
        fieldNames = dict()
        for key, value in iteritems(self._objects):
            fieldNames.update({
                key: [field for field in value[0].keys() if isField(field)]
                })
        self.lastDay= ns()
        for key, value in fieldNames.items():
            self.lastDay.update({
                key: field2date(sorted(fieldNames[key])[-1])
            })


    # TODO: Change name datum -> metric
    def getLastDay(self, datum):
        return self.lastDay[datum]

    def get(self, datum, dates, filters):

        objects = self._objects[datum]
        missing_dates = missingDates(includedDatesObject(objects), dates)
        if missing_dates:
            raise MissingDateError(missing_dates)

        filtered_tuples = locationFilter(objects, filters)

        return filtered_tuples


    def update(self, datum, content):

        _data = tablib.Dataset()
        _data.dict = self._objects[datum]
        _content = tablib.Dataset()
        _content.dict = content
        addedDates = sorted(includedDates(content), reverse=True)
        if addedDates and addedDates[0] > self.lastDay[datum]:
            self.lastDay[datum] = addedDates[0]
        addObjects(self._objects[datum], content)

import dbconfig as config
import os.path
import glob

def loadCsvSource(relativePath='../data/metrics'):
    myPath = os.path.abspath(os.path.dirname(__file__))
    dataPath = os.path.join(myPath, relativePath)
    datums = ns()
    for datafile in glob.glob(os.path.join(dataPath,'*.tsv')):
        datum = os.path.splitext(os.path.basename(datafile))[0]
        with open(datafile) as f:
            csvFile = f.read()
        datums[datum] = csvFile
    return CsvSource(datums)


