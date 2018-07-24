# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from dbutils import csvTable
from distribution import (
    parse_tsv,
    tuples2objects,
    )


data = None

class CsvSource():
    
    def __init__(self, content):
        self.data = content

    def extract(self, field, dates):

        tuples = parse_tsv(self.data)

        headersPerEliminar = [
            index for index, value in enumerate(tuples[0])
            if value.startswith('count_') and value[len('count_'):].replace('_','-') not in dates
        ]

        return [
            [element for index, element in enumerate(l) if index not in headersPerEliminar]
            for l in tuples
        ]


