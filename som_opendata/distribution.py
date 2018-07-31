# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from yamlns.dateutils import Date as isoDate

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
        isoDate(k[len('count_'):].replace('_', ''))
        for k in entry.keys()
        if k.startswith('count_')
        ]


def aggregate(entries, detail = 'world'):
    """
        Aggregates a list of entries by geographical scopes:
        Country, CCAA, state, city.
    """

    entry = entries[0]
    dates = state_dates(entry)

    result = ns ()
    result.dates = dates
    result.data = [0 for e in dates]

    for entry in entries:

        entry.count = [
            int(entry['count_'+date.isoDate.replace('-','_')])
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

    r = objectList

    for k, v in typeFilter.iteritems():
        r = [
            e for e in r if sum([i in e[k] for i in v]) > 0
        ]

    return r


def pickDates(tuples, dates):

    headersPerEliminar = [
        index for index, value in enumerate(tuples[0])
        if value.startswith('count_') and value[len('count_'):].replace('_','-') not in dates
    ]

    return [
        [element for index, element in enumerate(l) if index not in headersPerEliminar]
        for l in tuples
    ]

# vim: et sw=4 ts=4
