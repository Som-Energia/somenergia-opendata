# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from source import Source


class IntelligentSource(Source):
    
    data = None

    def __init__(self, content):
        self.data = content


    def get(self, datum, dates, filters):

        pass


    def set(self, datum, content):

        pass
