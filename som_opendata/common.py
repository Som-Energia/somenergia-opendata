#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta as delta
from yamlns.dateutils import Date
import os

def dateSequence(first, last):
    first = Date(first or Date.today())
    last = Date(last or first)
    interval = delta(last,first)
    months = interval.months + interval.years*12 + 1
    return [
        first + delta(months=n)
        for n in xrange(0, months)
        ]

def relative(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__),path))


def readQuery(query):
    with open(relative(query+".sql"), 'r') as queryfile:
        return queryfile.read().rstrip()


# vim: et ts=4 sw=4
