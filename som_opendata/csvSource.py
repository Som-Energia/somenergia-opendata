# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from dbutils import csvTable
from distribution import (
    parse_tsv,
    tuples2objects,
    locationFilter,
    pickDates,
    missedDates,
    findTuple,
    )
from source import Source
from missingDataError import MissingDataError

staticColumns = 8

class CsvSource(Source):
    
    data = None

    def __init__(self, content):
        self.data = content


    # TODO: Refactor --> "1 sol raise"
    def get(self, datum, dates, filters):

        tuples = parse_tsv(self.data[datum])

        if not tuples:
            raise MissingDataError([], dates, None)

        filtered_dates = pickDates(tuples, dates)

        if not filtered_dates or len(filtered_dates[0]) < staticColumns + len(dates):
            raise MissingDataError(locationFilter(tuples2objects(filtered_dates), filters), missedDates(tuples, dates), None)

        objectList = tuples2objects(filtered_dates)
        filtered_tuples = locationFilter(objectList, filters)
        if not filtered_tuples:
            raise MissingDataError(filtered_tuples, None, None)

        return filtered_tuples


    def set(self, datum, content):

        # ??????????
        # self.data[datum] += '\n' + '\n'.join('\t'.join(row) for row in content)

        oldHeaders = self.data[datum].split('\n')[0].split('\t') # amb l'anterior
        tuples = parse_tsv(self.data[datum])
        newHeaders = content[0].keys()
        newDatum = []
        newDatum.append(oldHeaders + [  header 
                                        for header in newHeaders
                                        if header not in oldHeaders
                                     ]
        )

        for _ns in content:
            t = findTuple(_ns, oldHeaders, tuples)
            t = t + [None] * (len(newHeaders) - len(oldHeaders))
            for index, elem_header in enumerate(newHeaders):
                t[index] = _ns[elem_header]
            newDatum.append(t)

        self.data[datum] = '\n'.join('\t'.join(elem for elem in _tuple) for _tuple in newDatum)

        #if len(content[0]) > len(self.data[datum].split('\n')[0].split('\t')):
#        #    # Afegir columnes
#        #    pass
#
#        #if len(content) > len(self.data[datum].split('\n')) - 1:
#        #    # Afegir rows
#
        #    self.data[datum] += '\n' + '\n'.join('\t'.join(row) for row in content)