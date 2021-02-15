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
    includedDatesObject,
    date2field,
    addObjects,
    field2date,
    isField,
    getAggregated,
    )
from .local_groups import LocalGroups
from .errors import (
    MissingDateError,
    AliasNotFoundError,
    )
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
            metric : tuples2objects(parse_tsv(data))
            for metric, data in iteritems(self.data)
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


    def getLastDay(self, metric):
        return self.lastDay[metric]

    def get(self, metric, dates, filters):

        objects = self._objects[metric]
        missing_dates = missingDates(includedDatesObject(objects), dates)
        if missing_dates:
            raise MissingDateError(missing_dates)

        filters = self.resolveAliases(**filters)
        filters = self.translateFilter(**filters)
        filtered_tuples = locationFilter(objects, filters)

        return filtered_tuples


    def update(self, metric, content):
        getAggregated.cache_clear()

        _data = tablib.Dataset()
        _data.dict = self._objects[metric]
        _content = tablib.Dataset()
        _content.dict = content
        addedDates = sorted(includedDates(content), reverse=True)
        if addedDates and addedDates[0] > self.lastDay[metric]:
            self.lastDay[metric] = addedDates[0]
        addObjects(self._objects[metric], content)

    def geolevelOptions(self, geolevel, **filters):
        filters = self.resolveAliases(**filters)
        filters = self.translateFilter(**filters)
        if geolevel in self._aliases:
            alias=self._aliases[geolevel]
            filteredCities = [
                line
                for metricLines in self._objects.values()
                for line in locationFilter(metricLines, filters)
                ]
            return ns(
                (aliascode, aliastext)
                for aliascode, aliastext in alias.getLocalGroups()
                if not filters or locationFilter(filteredCities,
                    self.translateFilter(**alias.data[aliascode].alias))
            )

        for plural, singular, codefield, namefield in common.aggregation_levels:
            if singular == geolevel: break
        else:
            # TODO: proper exception
            raise Exception("Not such geolevel '{}'".format(geolevel))

        return ns(
            (line[codefield], line[namefield])
            for tuples in self._objects.values()
            for line in locationFilter(tuples, filters)
        )

    def translateFilter(self, **filters):
        """Transforms public filter keys such as state, country...
        to the ones used to hold the fields in csv implementation
        codi_provincia, codi_pais..."""
        translated=ns()
        untranslated = set(filters.keys())
        for plural, singular, codefield, namefield in common.aggregation_levels:
            if singular not in filters:
                continue
            translated[codefield] = filters[singular]
            untranslated.remove(singular)

        for key in untranslated:
            # TODO: proper exception
            raise Exception("Not such geolevel '{}'".format(key))

        return translated

    def resolveAliases(self, **filters):
        """Rewrites filters turning alias fields (localgroups, county...)
        into its equivalent in actual geolevels (country, ccaa, state, city...)
        """
        result = dict()
        for originalField, originalValues in filters.items():
            if originalField not in self._aliases:
                result.setdefault(originalField, []).extend(originalValues)
                continue
            alias = self._aliases[originalField].data
            for originalValue in originalValues:
                if originalValue not in alias:
                    raise AliasNotFoundError(originalField, originalValue)
                for realField, realValues in alias[originalValue].alias.items():
                    result.setdefault(realField, []).extend(realValues)

        return result


import dbconfig as config
import os.path
import glob

def loadCsvSource(relativePath='../data/metrics', aliases={}):
    myPath = os.path.abspath(os.path.dirname(__file__))
    dataPath = os.path.join(myPath, relativePath)
    metrics = ns()
    for datafile in glob.glob(os.path.join(dataPath,'*.tsv')):
        metric = os.path.splitext(os.path.basename(datafile))[0]
        with open(datafile) as f:
            csvFile = f.read()
        metrics[metric] = csvFile
    return CsvSource(metrics, aliases=aliases)

# vim: et sw=4 ts=4
