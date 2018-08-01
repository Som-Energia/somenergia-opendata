# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from dbutils import csvTable
from distribution import (
    parse_tsv,
    tuples2objects,
    locationFilter,
    pickDates,
    )



class CsvSource():
    
    data = None

    def __init__(self, content):
        self.data = content


    def get(self, datum, dates, filters):

        tuples = parse_tsv(self.data)

        filtered_tuples = locationFilter(tuples, filters)

        if not filtered_tuples: return []

        return pickDates(filtered_tuples, dates)


    def set(self, datum, content):

        self.data += '\n' + '\t'.join(content)

