# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from dbutils import csvTable
from distribution import (
    parse_tsv,
    tuples2objects,
    locationFilter,
    pickDates,
    )
from source import Source
from missingDataError import MissingDataError

staticColumns = 8

class CsvSource(Source):
    
    data = None

    def __init__(self, content):
        self.data = content


    def get(self, datum, dates, filters):

        tuples = parse_tsv(self.data[datum])

        if not tuples or len(tuples[0])<len(dates)+8: raise MissingDataError(tuples, None, None)

        filtered_tuples = locationFilter(tuples, filters)

        if not filtered_tuples: raise MissingDataError(filtered_tuples, None, None)

        result = pickDates(filtered_tuples, dates)

        if not result: raise MissingDataError(result, None, None)

        return result

    def set(self, datum, content):

        self.data[datum] += '\n' + '\n'.join('\t'.join(row) for row in content)
