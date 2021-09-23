#!/usr/bin/env python3
import sys
from som_opendata.queries import (
    plantPowerSeries,
    plantProductionSeries,

    membersSeries,
    newMembersSeries,
    canceledMembersSeries,

    contractsSeries,
    newContractsSeries,
    canceledContractsSeries,

    selfConsumptionContractsSeries,
    newSelfConsumptionContractsSeries,
    canceledSelfConsumptionContractsSeries,

    publicContractsSeries,
    newPublicContractsSeries,
    canceledPublicContractsSeries,

    entityContractsSeries,
    newEntityContractsSeries,
    canceledEntityContractsSeries,

    homeownerCommunityContractsSeries,
    newHomeownerCommunityContractsSeries,
    canceledHomeownerCommunityContractsSeries,

    publicMembersSeries,
    newPublicMembersSeries,
    canceledPublicMembersSeries,

    entityMembersSeries,
    newEntityMembersSeries,
    canceledEntityMembersSeries,
)
from som_opendata.common import dateSequenceMonths
from yamlns.dateutils import Date
from dbutils import csvTable
import io
import os
from consolemsg import step, u

def nextFirstOfMonth():
    today = Date.today()
    if today.month == 12:
        return Date(today.year + 1, 1, 1)
    return Date(today.year, today.month+1, 1)

fromdate = Date('2010-01-01')

todate = nextFirstOfMonth()

dates=dateSequenceMonths(fromdate, todate)

metricGenerators = dict(
    plantpower=plantPowerSeries,
    plantproduction=plantProductionSeries,

    members=membersSeries,
    publicmembers=publicMembersSeries,
    entitymembers=entityMembersSeries,
    contracts=contractsSeries,
    selfconsumptioncontracts=selfConsumptionContractsSeries,
    publiccontracts=publicContractsSeries,
    entitycontracts=entityContractsSeries,
    homeownercommunitycontracts=homeownerCommunityContractsSeries,

    newmembers=newMembersSeries,
    newpublicmembers=newPublicMembersSeries,
    newentitymembers=newEntityMembersSeries,
    newcontracts=newContractsSeries,
    newpubliccontracts=newPublicContractsSeries,
    newentitycontracts=newEntityContractsSeries,
    newselfconsumptioncontracts=newSelfConsumptionContractsSeries,
    newhomeownercommunitycontracts=newHomeownerCommunityContractsSeries,

    canceledmembers=canceledMembersSeries,
    canceledpublicmembers=canceledPublicMembersSeries,
    canceledentitymembers=canceledEntityMembersSeries,
    canceledcontracts=canceledContractsSeries,
    canceledpubliccontracts=canceledPublicContractsSeries,
    canceledentitycontracts=canceledEntityContractsSeries,
    canceledselfconsumptioncontracts=canceledSelfConsumptionContractsSeries,
    canceledhomeownercommunitycontracts=canceledHomeownerCommunityContractsSeries,
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





