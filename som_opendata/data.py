# -*- coding: utf-8 -*-
from datafromcsv import (
    DataFromCSV,
)


class ExtractData(object):

    def __init__(self):
        pass

    def extractObjects(self, object, dates, source):
    
        first_source = source.extractObjects(object, dates)
        return first_source
