# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from source import Source
from missingDataError import MissingDataError


class IntelligentSource(Source):
    
    sources = []

    def __init__(self, sourceA, sourceB):
        self.sources.append(sourceA)
        self.sources.append(sourceB)


    def get(self, datum, dates, filters):

        index = 0

        for index, source in enumerate(self.sources):

            try:
                result = source.get(datum, dates, filters)
            except MissingDataError: pass
            else: break
        
        if result:
            for i in range(0, index): self.sources[i].set(datum, result)

        return result

    def set(self, datum, content):

        pass
