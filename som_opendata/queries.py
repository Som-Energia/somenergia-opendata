# coding=utf-8
import os
import psycopg2
import dbconfig as config
from dbutils import csvTable
from yamlns import namespace as ns
from yamlns.dateutils import Date
from pathlib import Path

"""
This module contains functions to compute metrics.
Metrics have to be computed aggregated by city and month.
"""

def readQuery(query):
    queryfile = Path(__file__).absolute().parent / 'queries' / (query + '.sql')
    return queryfile.read_text(encoding='utf8').rstrip()

def timeQuery(dates, queryfile, timeSlicer, dbhandler=csvTable):
    """
    Executes a query stored in queryfile
    extending it with a column for each passed date
    which aggregates rows by that date.
    The timeSlicer parameter tells whether to filter or not
    each row for a given date.
    """
    db = psycopg2.connect(**config.psycopg)
    query = readQuery(queryfile)
    query = query.format(','.join(
        timeSlicer(Date(adate))
        for adate in dates
        ))
    with db.cursor() as cursor :
        cursor.execute(query)
        return dbhandler(cursor)

def timeCityQuery(dates, queryfile, timeSlicer, dbhandler=csvTable):
    """
    Executes the query stored in `queryfile` as inner query of an enclosing
    query which aggregates inner results by field `city_id` and adds columns
    aggregating data for each date in `dates` as specified by `timeSlicer`.
    In order to work, the inner query is expected to generate fields
    `first_date`, `last_date` and `city_id`.
    """
    db = psycopg2.connect(**config.psycopg)
    innerQuery = readQuery(queryfile)
    counterFields = ','.join(
        timeSlicer(Date(adate))
        for adate in dates
    )
    query = readQuery('month_city_distribution')
    query = query.format(counterFields, innerQuery)
    with db.cursor() as cursor :
        cursor.execute(query)
        return dbhandler(cursor)

def activeItemAdder(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    sum(CASE
        WHEN item.first_date IS NULL THEN 0
        WHEN item.first_date >= '{adate}'::date THEN 0
        WHEN item.last_date is NULL then value
        WHEN item.last_date >= '{adate}'::date THEN value
        ELSE 0
        END) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def activeItemCounter(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    count(CASE
        WHEN item.first_date IS NULL THEN NULL
        WHEN item.first_date >= '{adate}'::date THEN NULL
        WHEN item.last_date is NULL then TRUE
        WHEN item.last_date >= '{adate}'::date THEN TRUE
        ELSE NULL
        END) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def activeItemLister(adate):
    """Debug substitute for activeItemCounter
    List ids instead of count them
    """
    # TODO: Unsafe substitution, use mogrify
    return """
    string_agg(CASE
        WHEN item.first_date IS NULL THEN NULL
        WHEN item.first_date >= '{adate}'::date THEN NULL
        WHEN item.last_date is NULL then item.id::text
        WHEN item.last_date >= '{adate}'::date THEN item.id::text
        ELSE NULL
        END, ',' ORDER BY item.id) AS ids_{adate:%Y_%m_%d}
""".format(adate=adate)

def newItemCounter(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    count(CASE
        WHEN item.first_date IS NULL THEN NULL
        WHEN item.first_date >= '{adate}'::date THEN NULL
        WHEN item.first_date <  '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE TRUE
        END) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def newItemLister(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    string_agg(CASE
        WHEN item.first_date IS NULL THEN NULL
        WHEN item.first_date >= '{adate}'::date THEN NULL
        WHEN item.first_date <  '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE item.id::text
        END, ',' ORDER BY item.id) AS ids_{adate:%Y_%m_%d}
""".format(adate=adate)

def canceledItemCounter(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    count(CASE
        WHEN item.last_date is NULL then NULL
        WHEN item.last_date >= '{adate}'::date THEN NULL
        WHEN item.last_date <  '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE TRUE
        END) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def canceledItemLister(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    string_agg(CASE
        WHEN item.last_date is NULL then NULL
        WHEN item.last_date >= '{adate}'::date THEN NULL
        WHEN item.last_date <  '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE item.id::text
        END, ',' ORDER BY item.id) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def contractsSeries(dates, dbhandler=csvTable):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts',
        timeSlicer=activeItemCounter,
        #timeSlicer=activeItemLister, # debug
        dbhandler=dbhandler,
    )

def newContractsSeries(dates, dbhandler=csvTable):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts',
        timeSlicer=newItemCounter,
        #timeSlicer=newItemLister, # debug
        dbhandler=dbhandler,
    )


def canceledContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts',
        timeSlicer=canceledItemCounter,
        #timeSlicer=canceledItemLister, # debug
        dbhandler=dbhandler,
    )

def selfConsumptionContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts_selfconsumption',
        timeSlicer=activeItemCounter,
        #timeSlicer=activeItemLister, # debug
        dbhandler=dbhandler,
    )

def newSelfConsumptionContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts_selfconsumption',
        timeSlicer=newItemCounter,
        #timeSlicer=newItemLister, # debug
        dbhandler=dbhandler,
    )

def canceledSelfConsumptionContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts_selfconsumption',
        timeSlicer=canceledItemCounter,
        #timeSlicer=canceledItemLister, # debug
        dbhandler=dbhandler,
    )

def homeownerCommunityContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts_homeowner_association',
        timeSlicer=activeItemCounter,
        #timeSlicer=activeItemLister, # debug
        dbhandler=dbhandler,
    )

def newHomeownerCommunityContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts_homeowner_association',
        timeSlicer=newItemCounter,
        #timeSlicer=newItemLister, # debug
        dbhandler=dbhandler,
    )

def canceledHomeownerCommunityContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts_homeowner_association',
        timeSlicer=canceledItemCounter,
        #timeSlicer=canceledItemLister, # debug
        dbhandler=dbhandler,
    )

def publicContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts_public_administration',
        timeSlicer=activeItemCounter,
        #timeSlicer=activeItemLister, # debug
        dbhandler=dbhandler,
    )

def newPublicContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts_public_administration',
        timeSlicer=newItemCounter,
        #timeSlicer=newItemLister, # debug
        dbhandler=dbhandler,
    )

def canceledPublicContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts_public_administration',
        timeSlicer=canceledItemCounter,
        #timeSlicer=canceledItemLister, # debug
        dbhandler=dbhandler,
    )

def entityContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts_legal_persons_and_business',
        timeSlicer=activeItemCounter,
        #timeSlicer=activeItemLister, # debug
        dbhandler=dbhandler,
    )

def newEntityContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts_legal_persons_and_business',
        timeSlicer=newItemCounter,
        #timeSlicer=newItemLister, # debug
        dbhandler=dbhandler,
    )

def canceledEntityContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='contracts_legal_persons_and_business',
        timeSlicer=canceledItemCounter,
        #timeSlicer=canceledItemLister, # debug
        dbhandler=dbhandler,
    )

def membersSeries(dates, dbhandler=csvTable, debug=False):
    return timeQuery(
        dates=dates,
        queryfile='members_distribution',
        timeSlicer=activeItemCounter,
        #timeSlicer=activeItemLister, # debug
        dbhandler=dbhandler,
    )

def newMembersSeries(dates, dbhandler=csvTable, debug=False):
    return timeQuery(
        dates=dates,
        queryfile='members_distribution',
        timeSlicer=newItemCounter,
        #timeSlicer=newItemLister, # debug
        dbhandler=dbhandler,
    )

def canceledMembersSeries(dates, dbhandler=csvTable, debug=False):
    return timeQuery(
        dates=dates,
        queryfile='members_distribution',
        timeSlicer=canceledItemCounter,
        #timeSlicer=canceledItemLister, # debug
        dbhandler=dbhandler,
    )


def publicMembersSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='members_public_administration',
        timeSlicer=activeItemCounter,
        #timeSlicer=activeItemLister, # debug
        dbhandler=dbhandler,
    )

def newPublicMembersSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='members_public_administration',
        timeSlicer=newItemCounter,
        #timeSlicer=newItemLister, # debug
        dbhandler=dbhandler,
    )

def canceledPublicMembersSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='members_public_administration',
        timeSlicer=canceledItemCounter,
        #timeSlicer=canceledItemLister, # debug
        dbhandler=dbhandler,
    )

def entityMembersSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='members_legal_persons',
        timeSlicer=activeItemCounter,
        #timeSlicer=activeItemLister, # debug
        dbhandler=dbhandler,
    )

def newEntityMembersSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='members_legal_persons',
        timeSlicer=newItemCounter,
        #timeSlicer=newItemLister, # debug
        dbhandler=dbhandler,
    )

def canceledEntityMembersSeries(dates, dbhandler=csvTable, debug=False):
    return timeCityQuery(
        dates=dates,
        queryfile='members_legal_persons',
        timeSlicer=canceledItemCounter,
        #timeSlicer=canceledItemLister, # debug
        dbhandler=dbhandler,
    )

def plantPowerSeries(dates, dbhandler=csvTable):
    return timeQuery(
        dates=dates,
        queryfile='plantpower',
        timeSlicer=activeItemAdder,
        #timeSlicer=activeItemLister, # debug
        dbhandler=dbhandler,
    )

def plantProductionAdder(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    (sum(CASE
        WHEN (energy.time::date + '1 month'::interval)::date = '{adate}'::date  THEN energy.export_energy_wh
        ELSE 0
        END)/1000)::integer AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def plantProductionSeries(dates, dbhandler=csvTable):
    """
    """
    db = psycopg2.connect(**config.plantmonitor_psycopg)
    query = readQuery('plantproduction')
    query = query.format(','.join(
        plantProductionAdder(Date(adate))
        for adate in dates
        ))
    with db.cursor() as cursor :
        cursor.execute(query)
        return dbhandler(cursor)

# vim: et sw=4 ts=4
