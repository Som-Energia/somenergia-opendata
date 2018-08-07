# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from source import Source
from missingDataError import MissingDataError


class IntelligentSource(Source):
    
   
    def __init__(self, sourceA, sourceB):
        self.sources = []
        self.sources.append(sourceA)
        self.sources.append(sourceB)


    def get(self, datum, dates, filters):

        index = 0
        result = []

        for index, source in enumerate(self.sources):

            try:
                result = source.get(datum, dates, filters)
            except MissingDataError as err:
                if err.data:
                    result = err.data
            else: break
        
        if not result:
            raise MissingDataError(result, dates, None)

        for i in range(0, index):
            self.sources[i].set(datum, result)

        return result

    def set(self, datum, content):

        pass
