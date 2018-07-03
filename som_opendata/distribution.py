# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from yamlns.dateutils import Date as isoDate



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


def aggregate(entries, detail = None):
    """
        Aggregates a list of entries by geographical scopes:
        Country, CCAA, state, city.
    """

    entry = entries[0]
    dates = state_dates(entry)

    result = ns (
        dates = dates,
        level = 'countries',
        countries = ns()
    )

    for entry in entries:

        entry.count = [
            int(entry['count_'+date.isoDate.replace('-','_')])
            for date in dates ]

        if detail != 'country':
            country = aggregate_level(
                entry, result, 'countries', 'codi_pais', 'pais')

            if detail != 'ccaa':
                ccaa = aggregate_level(
                    entry, country, 'ccaas', 'codi_ccaa', 'comunitat_autonoma')

                if detail != 'state':
                    provincia = aggregate_level(
                        entry, ccaa, 'states', 'codi_provincia', 'provincia')

                    if detail != 'city':
                        city = aggregate_level(
                            entry, provincia, 'cities', 'codi_ine', 'municipi')

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









import copy             

def idem(tipus, elemA, elemB):
     return elemA[tipus] == elemB[tipus]


def eliminar(item, l):
    return list(
        filter(lambda e: not idem('codi_ine',item,e), l)
        )

def escollirINES(l):
    llista = []
    lTractar = copy.deepcopy(l)
    for item in lTractar:
        if not contains(item,llista):
            if esUnic(item,l):                              
                llista.append(item)
            else:
                itemAgregat = agregar(item,l)
                eliminar(item,lTractar)
                llista.append(itemAgregat)
    return llista


def esUnic(item, l):
    count = 0
    for e in l:
        if count == 0 and idem('codi_ine',item,e):
            count += 1
        elif count == 1 and idem('codi_ine',item,e):
            return False
    return True


def agregar(item, l):
    newItem = copy.deepcopy(item)
    newItem.quants = 0
    for e in l:
        if idem('codi_ine',item,e):
            newItem.quants += int(e.quants)
    return newItem


def contains(item, l):
    for e in l:
        if idem('codi_ine',item,e):
            return True
    return False




def packageCountries(l):
    d = ns()
    for e in l:
        if not e.codi_pais in d:
            d[e.codi_pais] = ns()
    return d


def packageCCAA(l, d):
    for e in l:
        if not e.codi_ccaa in d[e.codi_pais]:
            d[e.codi_pais][e.codi_ccaa] = ns()
    return d


def packageStates(l, d):
    for e in l:
        if not e.codi_provincia in d[e.codi_pais][e.codi_ccaa]:
            d[e.codi_pais][e.codi_ccaa][e.codi_provincia] = ns()
    return d


def packageCities(l, d):
    for e in l:
        if not e.codi_ine in d[e.codi_pais][e.codi_ccaa][e.codi_provincia]:
            d[e.codi_pais][e.codi_ccaa][e.codi_provincia][e.codi_ine] = e
    return d


def select_only_city(input, ine):
    r = tuples2objects(parse_tsv(input))
    return [item for item in r if item.codi_ine == ine]




# vim: et sw=4 ts=4
