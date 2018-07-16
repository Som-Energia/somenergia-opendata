# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from dbutils import csvTable
from distribution import (
    parse_tsv,
    tuples2objects,
    )



import io

with io.open('som_opendata/utils/membersSparse_many-expected') as f:
    data = f.read()


class DataFromCSV():

    def __init__(self):
        return None

    def eliminateIrrelevantDates(self, dataWithDates, dates):

        headersPerEliminar = [
            index for index, value in enumerate(dataWithDates[0]) 
            if 'count' in value and not any([value == 'count_'+date for date in dates])
        ]

        return [
            [element for index, element in enumerate(l) if index not in headersPerEliminar]
            for l in dataWithDates
        ]

    #TODO: Cal buscar diferents csv en funcio de 'object'
    def extractObjects(self, object, dates):

        res = parse_tsv(data)

        dataImportant = self.eliminateIrrelevantDates(res,dates)

        if len(dataImportant[0]) <= 8:
            return []
        else:
            return dataImportant

