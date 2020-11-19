# -*- coding: utf-8 -*-
import tablib
from yamlns import namespace as ns
from future.utils import iteritems

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
    cachedGetAggregated,
    )
from .local_groups import LocalGroups
from .errors import MissingDateError
from . import common

class CsvSource(object):
    
    data = None

    def __init__(self, content, aliases=ns()):
        self._aliases = ns(
            (k, LocalGroups(v, k))
            for k,v in aliases.items()
        )
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

        filters = self.translateFilter(**filters)

        filtered_tuples = locationFilter(objects, filters)

        return filtered_tuples


    def update(self, datum, content):
        cachedGetAggregated.cache_clear()

        _data = tablib.Dataset()
        _data.dict = self._objects[datum]
        _content = tablib.Dataset()
        _content.dict = content
        addedDates = sorted(includedDates(content), reverse=True)
        if addedDates and addedDates[0] > self.lastDay[datum]:
            self.lastDay[datum] = addedDates[0]
        addObjects(self._objects[datum], content)

    def geolevelOptions(self, geolevel, **filters):
        filters = self.translateFilter(**filters)
        if geolevel in self._aliases:
            return ns(self._aliases[geolevel].getLocalGroups())

        for plural, singular, codefield, namefield in common.aggregation_levels:
            if singular == geolevel: break
        else:
            raise Exception("Not such geolevel '{}'".format(geolevel))

        return ns(
            (line[codefield], line[namefield])
            for tuples in self._objects.values()
            for line in locationFilter(tuples, filters)
        )

    def translateFilter(self, **filters):
        """Transforms public filter keys such as state, country...
        to the ones used to hold the fields in csv implementation."""
        translated=ns()
        untranslated = set(filters.keys())
        for plural, singular, codefield, namefield in common.aggregation_levels:
            if singular not in filters:
                continue
            # TODO
            filtervalues = translated.setdefault(codefield, [])
            filtervalues += filters[singular]
            untranslated.remove(singular)

        for key in untranslated:
            raise Exception("Not such geolevel '{}'".format(key))

        return translated


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

# vim: et sw=4 ts=4
