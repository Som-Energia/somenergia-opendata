# -*- coding: utf-8 -*-
from yamlns.dateutils import Date as isoDate
from yamlns import namespace as ns
from functools import lru_cache
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

def aggregate(entries, detail='world', timeDomain=None):
    """
        Aggregates a list of entries by geographical scopes:
        Country, CCAA, state, city.
    """
    if not entries: return ns()

    if not timeDomain:
        requestDates = sourceDates = headerDates(entries[0])
    else:
        requestDates = timeDomain.requestDates
        sourceDates = timeDomain.sourceDates

    result = ns ()
    result.dates = [isoDate(d) for d in requestDates]
    dateFields = [date2field(date) for date in sourceDates]
    result['values'] = [0] * len(requestDates)

    for entry in entries:
        entry.count = [
            int(entry[field])
            for field in dateFields
        ]
        if timeDomain: entry.count = timeDomain.aggregate(entry.count)

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


def aggregated2table(data):
    yield aggregated2tableHeader(data.dates, data)
    yield from aggregated2tableContent(data)

def findSublevel(region):
    for key, level in common.geolevels.items():
        if level.get('plural', key+'s') in region:
            return key

def aggregated2tableHeader(dates, region, geoheaders=[]):
    sublevel = findSublevel(region)
    if sublevel is None:
        return [*geoheaders, *dates]
    plural = common.geolevels[sublevel].plural
    subregions = region[plural]
    for key, subregion in subregions.items():
        return aggregated2tableHeader(
            dates=dates,
            region=subregion,
            geoheaders=[*geoheaders, sublevel+'_code', sublevel],
        )

def aggregated2tableContent(region, parentcodenames=[]):
    sublevel = findSublevel(region)
    if sublevel is None: # leaf
        yield [*parentcodenames, *region['values']]
        return
    plural = common.geolevels[sublevel].plural
    subregions = region[plural]
    for key, subregion in subregions.items():
        yield from aggregated2tableContent(
            region=subregion,
            parentcodenames=[*parentcodenames, key, subregion.name]
        )

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

def distributionKey(source, metric, timeDomain, location_filter, geolevel):
    return (
        source,
        metric,
        tuple(timeDomain.requestDates),
        tuple(
            (k,tuple(sorted(v)))
            for k,v in sorted(location_filter.items())
        ),
        geolevel,
    )

def getAggregated(source, metric, timeDomain, location_filter, geolevel, mutable):
    if not hasattr(getAggregated, 'cache'):
        cache_clear()

    if not mutable:
        key = distributionKey(source, metric, timeDomain, location_filter, geolevel)
        if key in getAggregated.cache:
            getAggregated.cache_hits+=1
            return getAggregated.cache[key]
        getAggregated.cache_misses+=1

    filtered_objects = source.get(metric, timeDomain.sourceDates, location_filter)
    result = aggregate(filtered_objects, geolevel, timeDomain)

    if not mutable:
        getAggregated.cache[key] = result
    return result


def cache_clear():
    getAggregated.cache = {}
    getAggregated.cache_hits = 0
    getAggregated.cache_misses = 0

getAggregated.cache_clear = cache_clear




# vim: et sw=4 ts=4
