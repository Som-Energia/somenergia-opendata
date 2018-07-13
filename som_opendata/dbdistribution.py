# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from dbutils import csvTable
from distribution import (
    parse_tsv,
    tuples2objects,
    )



import io

with io.open('./som_opendata/utils/dbexample') as f:
    data = f.read()


def eliminateIrrelevantDates(dataWithDates,dates):

    headersPerEliminar = [
        index for index, value in enumerate(dataWithDates[0]) 
        if 'count' in value and not any([value == 'count_'+date for date in dates])
    ]

    return [
        [element for index, element in enumerate(l) if index not in headersPerEliminar]
        for l in dataWithDates
    ]


def extractObjects(object, dates):

    res = parse_tsv(data)

    dataImportant = eliminateIrrelevantDates(res,dates)

    if len(dataImportant[0]) <= 8:
        return []
    else:
        return dataImportant

