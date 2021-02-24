#!/usr/bin/env python
import sys
from som_opendata.queries import (
    membersSeries,
    contractsSeries,
    newContractsSeries,
    canceledContractsSeries,
    selfConsumptionContractsSeries,
    newSelfConsumptionContractsSeries,
    canceledSelfConsumptionContractsSeries,
    newMembersSeries,
    canceledMembersSeries,
)
from som_opendata.common import dateSequenceMonths
from yamlns.dateutils import Date
from dbutils import csvTable
import io
import os
from consolemsg import step, u


fromdate = Date('2010-01-01')
todate = Date.today()

dates=dateSequenceMonths(fromdate, todate)

metricGenerators = dict(
    members=membersSeries,
    contracts=contractsSeries,
    selfconsumptioncontracts=selfConsumptionContractsSeries,
    newcontracts=newContractsSeries,
    canceledcontracts=canceledContractsSeries,
    newselfconsumptioncontracts=newSelfConsumptionContractsSeries,
    canceledselfconsumptioncontracts=canceledSelfConsumptionContractsSeries,
    newmembers=newMembersSeries,
    canceledmembers=canceledMembersSeries,
)


for metric, generator in metricGenerators.items():

    step("Generating {}...", metric)

    filename = '{metric}{frm}{to}.tsv'.format(
        metric = metric,
        frm = '-'+str(fromdate) if fromdate else '',
        to  = '-'+str(todate) if todate else '',
    )
    result = generator(dates)
    with io.open(filename,'w') as f:
        f.write(u(result))

    linkname = 'data/metrics/{}.tsv'.format(metric)

    with io.open(linkname,'w') as f:
        f.write(u(result))





