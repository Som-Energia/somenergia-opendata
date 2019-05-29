#!/usr/bin/env python
import sys
from som_opendata.oldapi import (
    membersSparse,
    contractsSeries,
)
from som_opendata.common import (
    dateSequenceMonths,
    readQuery,
    dateSequenceWeeksMonths,
    utf8,
    )

from yamlns.dateutils import Date
from dbutils import csvTable
import io
import os
from consolemsg import step


fromdate = Date('2010-01-01')
todate = Date.today()

dates=dateSequenceMonths(fromdate, todate)


for metric, generator in dict(
        members=membersSparse,
        contracts=contractsSeries,
        ).items():

    step("Generating {}...", metric)

    filename = '{metric}{frm}{to}.tsv'.format(
        metric = metric,
        frm = '-'+str(fromdate) if fromdate else '',
        to  = '-'+str(todate) if todate else '',
    )
    result = generator(dates)
    with io.open(filename,'w') as f:
        f.write(utf8(result))

    linkname = 'data/{}.tsv'.format(metric)

    with io.open(linkname,'w') as f:
        f.write(utf8(result))





