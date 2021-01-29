# -*- coding: utf-8 -*-
from yamlns.dateutils import Date as isoDate
from yamlns import namespace as ns
from functools import lru_cache
from frozendict import frozendict
from . import common

def parse_tsv(tsv_data):
    """
        Parses a TSV file content into a header and a list of tuples.
        Ignores empty lines.
    """
    return [
        [item.strip() for item in line.split('\t')]
        for line in tsv_data.split('\n')
        if line.strip()
        ]

def tuples2objects(tuples):
    """
        Turns a list of tuples including the first one with the column names,
        into a list of entries (ns objects) having the colunm names as
        attribute names.
    """
    if not tuples: return []
    headers = tuples[0]
    data = tuples[1:]
    return [
        ns([
            (header, value)
            for header, value in zip(headers, item)
            ])
        for item in data
        ]


def headerDates(entry):
    """
        Returns the dates included in the entry
    """
    return [
        field2date(k)
        for k in entry.keys()
        if isField(k)
        ]

def aggregate(entries, detail='world', dates=None):
    """
        Aggregates a list of entries by geographical scopes:
        Country, CCAA, state, city.
    """
    if not entries: return ns()

    if not dates:
        dates = headerDates(entries[0])

    result = ns ()
    result.dates = [isoDate(d) for d in dates]
    dateFields = [date2field(date) for date in dates]
    result['values'] = [0] * len(dates)

    for entry in entries:
        entry.count = [
            int(entry[field])
            for field in dateFields]

        result['values'] = [a+b for a,b in zip(result['values'], entry.count)]
        if detail == 'world': continue
        current = result

        for level_name, level_single, codi, name in common.aggregation_levels:
            current = aggregate_level(
                entry, current, level_name, codi, name)
            if detail == level_single: break

    return result


def aggregate_level(entry, parent, sibbling_attr, code_attr, name_attr):
    sibblings = parent.setdefault(sibbling_attr, ns())
    name = entry[name_attr]
    code = entry[code_attr]
    if code not in sibblings:
        result = sibblings[code] = ns()
        result.name = name
        result['values'] = entry.count[:]
        return result

    result = sibblings[code]
    result['values'] = [a+b for a,b in zip(result['values'], entry.count)]
    return result


def locationFilter(entries, filters):
    if not filters: return entries

    return [
        entry
        for entry in entries
        if any(
            entry[field] in allowedValues
            for field, allowedValues in filters.items()
        )
    ]


def includedDates(tuples):

    if not tuples: return []

    return [ field2date(header)
        for header in tuples[0]
        if isField(header) and
        validateStringDate(field2date(header))
        ]

def includedDatesObject(objects):
    
    if not objects: return []

    return [ field2date(key)
        for key, value in objects[0].items()
        if isField(key) and validateStringDate(field2date(key))
    ]



def validateStringDate(date):

    try:
        isoDate(date)
    except ValueError:
        return False

    return True

def field2date(field):
    return field[len('count_'):].replace('_', '-')

def date2field(date):
    return 'count_' + date.replace('-', '_')

def isField(field):
    return field.startswith('count_')

def missingDates(datesExist, datesRequest):
    return list(set(datesRequest) - set(datesExist))

def findObject(objectList, key, value):
     for o in objectList:
         if o[key] == value:
             return o

def addObjects(data, content):
    for _object in content:
        _d = findObject(data, 'codi_ine', _object['codi_ine'])
        if not _d:
            aux = ns(_object)
            dates = missingDates(includedDatesObject(content), includedDatesObject(data))
            for date in dates:
                aux[date2field(date)] = '0'
            data.append(aux)
        else:
            addCounts(_d, ((key, value)
                for key, value in _object.items() if isField(key)
                ))

def addCounts(dictionary, newElements):
    for (key, value) in newElements:
        dictionary[key] = value


@lru_cache()
def cachedGetAggregated(source, metric, request_dates, location_filter, geolevel):
    filtered_objects = source.get(metric, request_dates, location_filter)
    return aggregate(filtered_objects, geolevel, request_dates)


def getAggregated(source, metric, request_dates, location_filter, geolevel, mutable):

    if (mutable):
        filtered_objects = source.get(metric, request_dates, location_filter)
        return aggregate(filtered_objects, geolevel, request_dates)

    location_filter = frozendict(sorted(
        (k,tuple(sorted(v)))
        for k,v in location_filter.items()
    ))
    return cachedGetAggregated(source, metric, tuple(request_dates), location_filter, geolevel)

# vim: et sw=4 ts=4
