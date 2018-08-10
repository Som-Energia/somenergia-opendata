# -*- coding: utf-8 -*-
from yamlns.dateutils import Date as isoDate
from yamlns import namespace as ns

aggregation_levels = [
    ('countries', 'country', 'codi_pais', 'pais'),
    ('ccaas', 'ccaa', 'codi_ccaa', 'comunitat_autonoma'),
    ('states', 'state', 'codi_provincia', 'provincia'),
    ('cities', 'city', 'codi_ine', 'municipi'),
    ]

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


def state_dates(entry):
    """
        Returns the dates included in the entry
    """
    return [
        isoDate(field2date(k))
        for k in entry.keys()
        if isField(k)
        ]


def aggregate(entries, detail = 'world'):
    """
        Aggregates a list of entries by geographical scopes:
        Country, CCAA, state, city.
    """
    if not entries: return []

    entry = entries[0]
    dates = state_dates(entry)

    result = ns ()
    result.dates = dates
    result.data = [0 for e in dates]

    for entry in entries:

        entry.count = [
            int(entry[date2field(date.isoDate)])
            for date in dates ]

        result.data = [a+b for a,b in zip(result.data, entry.count)]
        if detail == 'world': continue
        current = result
        
        for level_name, level_single, codi, name in aggregation_levels:
            current = aggregate_level(
                entry, current, level_name, codi, name)
            if detail == level_name: break

    return result


def aggregate_level(entry, parent, sibbling_attr, code_attr, name_attr):
    sibblings = parent.setdefault(sibbling_attr, ns())
    name = entry[name_attr]
    code = entry[code_attr]
    if code in sibblings:
        result = sibblings[code]
        result.data = [a+b for a,b in zip(result.data, entry.count)]
    else:
        result = sibblings[code] = ns()
        result.name = name
        result.data = entry.count[:]

    return result


def locationFilter(objectList, typeFilter):
    if not typeFilter: return objectList
    
    return [
        entry
        for entry in objectList
        if any(
             entry[k] in v
             for k,v in typeFilter.iteritems()
        )
    ]


def pickDates(tuples, dates):

    headersPerEliminar = [
        index for index, value in enumerate(tuples[0])
        if isField(value) and field2date(value) not in dates
    ]

    #if len(tuples[0]) - len(headersPerEliminar) < len(dates) + 8: 
    #    return []
    if len(tuples[0]) - len(headersPerEliminar) == 8:
        return []

    return [
        [element for index, element in enumerate(l) if index not in headersPerEliminar]
        for l in tuples
    ]


def findTuple(namespace, hOld, tuples):
    values = [
        value
        for key, value in namespace.iteritems()
        if not isField(key)
        ]
    for t in tuples:
        if all(value in t for value in values):
            return t

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
        for key, value in objects[0].iteritems()
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

def removeDates(objects, dates):
    return [
        removeCounts(o, [date2field(d) for d in dates])
        for o in objects
    ]

def removeCounts(_object, counts):
    ret = ns()
    for key, value in _object.iteritems():
        if key not in counts:
            ret[key] = value
    return ret

def findObject(objectList, key, value):
     for o in objectList:
         if o[key] == value:
             return o

#TODO : TEST IT
def addObjects(data, content):
    if len(data) != len(content):
        index = 0
        for _object in content:
            _d = findObject(data, 'codi_ine', _object['codi_ine'])
            if not _d:
                aux = ns(_object)
                dates = missingDates(includedDatesObject(content), includedDatesObject(data))
                for date in dates:
                    aux[date2field(date)] = '0'
                data.append(aux)

# vim: et sw=4 ts=4
