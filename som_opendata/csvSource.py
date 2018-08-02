# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from dbutils import csvTable
from distribution import (
    parse_tsv,
    tuples2objects,
    locationFilter,
    pickDates,
    missedDates,
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
        if not tuples or len(tuples[0])<len(dates)+8:
            raise MissingDataError(tuples, missedDates(tuples, dates), None)
        
        filtered_dates = pickDates(tuples, dates)
        if not filtered_dates: 
            raise MissingDataError(filtered_dates, None, None)
        
        objectList = tuples2objects(filtered_dates)
        filtered_tuples = locationFilter(objectList, filters)
        if not filtered_tuples: 
            raise MissingDataError(filtered_tuples, None, None)

        return filtered_tuples


    def set(self, datum, content):

        self.data[datum] += '\n' + '\n'.join('\t'.join(row) for row in content)

