# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from source import Source


class IntelligentSource(Source):
    
    sources = []

    def __init__(self, sourceA, sourceB):
        self.sources.append(sourceA)
        self.sources.append(sourceB)


    def get(self, datum, dates, filters):

        return self.sources[0].get(datum, dates, filters)


    def set(self, datum, content):

        pass
