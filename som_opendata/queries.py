# coding=utf-8
import os
import psycopg2
import dbconfig as config
from dbutils import csvTable
from yamlns import namespace as ns
from yamlns.dateutils import Date

"""
This module contains functions to compute metrics.
Metrics have to be computed aggregated by city and month.
"""

def relative(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


def readQuery(query):
    with open(relative(query + '.sql'), 'r') as queryfile:
        return queryfile.read().rstrip()


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


def activeContractsCounter(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    count(CASE
        WHEN polissa.data_alta IS NULL THEN NULL
        WHEN polissa.data_alta > '{adate}'::date THEN NULL
        WHEN polissa.data_baixa is NULL then TRUE
        WHEN polissa.data_baixa > '{adate}'::date THEN TRUE
        ELSE NULL
        END) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def activeContractsLister(adate):
    """Debug substitute for activeContractsCounter
    List ids instead of count them
    """
    # TODO: Unsafe substitution, use mogrify
    return """
    string_agg(CASE
        WHEN polissa.data_alta IS NULL THEN NULL
        WHEN polissa.data_alta > '{adate}'::date THEN NULL
        WHEN polissa.data_baixa is NULL then polissa.id::text
        WHEN polissa.data_baixa > '{adate}'::date THEN polissa.id::text
        ELSE NULL
        END, ',' ORDER BY polissa.id) AS ids_{adate:%Y_%m_%d}
""".format(adate=adate)

def contractsSeries(dates, dbhandler=csvTable):
    return timeQuery(
        dates=dates,
        queryfile='contract_distribution',
        timeSlicer=activeContractsCounter,
        #timeSlicer=activeContractsLister, # debug
        dbhandler=dbhandler,
    )

def newContractsCounter(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    count(CASE
        WHEN polissa.data_alta IS NULL THEN NULL
        WHEN polissa.data_alta > '{adate}'::date THEN NULL
        WHEN polissa.data_alta <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE TRUE
        END) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def newContractsLister(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    string_agg(CASE
        WHEN polissa.data_alta IS NULL THEN NULL
        WHEN polissa.data_alta > '{adate}'::date THEN NULL
        WHEN polissa.data_alta <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE polissa.id::text
        END, ',' ORDER BY polissa.id) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def newContractsSeries(dates, dbhandler=csvTable):
    return timeQuery(
        dates=dates,
        queryfile='contract_distribution',
        timeSlicer=newContractsCounter,
        #timeSlicer=newContractsLister, # debug
        dbhandler=dbhandler,
    )


def canceledContractsCounter(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    count(CASE
        WHEN polissa.data_baixa is NULL then NULL
        WHEN polissa.data_baixa > '{adate}'::date THEN NULL
        WHEN polissa.data_baixa <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE TRUE
        END) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def canceledContractsLister(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    string_agg(CASE
        WHEN polissa.data_baixa is NULL then NULL
        WHEN polissa.data_baixa > '{adate}'::date THEN NULL
        WHEN polissa.data_baixa <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE polissa.id::text
        END, ',' ORDER BY polissa.id) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def canceledContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeQuery(
        dates=dates,
        queryfile='contract_distribution',
        timeSlicer=canceledContractsCounter,
        #timeSlicer=canceledContractsLister, # debug
        dbhandler=dbhandler,
    )

def activeItemCounter(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    count(CASE
        WHEN item.first_date IS NULL THEN NULL
        WHEN item.first_date > '{adate}'::date THEN NULL
        WHEN item.last_date is NULL then TRUE
        WHEN item.last_date > '{adate}'::date THEN TRUE
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
        WHEN item.first_date > '{adate}'::date THEN NULL
        WHEN item.last_date is NULL then item.id::text
        WHEN item.last_date > '{adate}'::date THEN item.id::text
        ELSE NULL
        END, ',' ORDER BY item.id) AS ids_{adate:%Y_%m_%d}
""".format(adate=adate)

def newItemCounter(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    count(CASE
        WHEN item.first_date IS NULL THEN NULL
        WHEN item.first_date > '{adate}'::date THEN NULL
        WHEN item.first_date <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE TRUE
        END) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def newItemLister(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    string_agg(CASE
        WHEN item.first_date IS NULL THEN NULL
        WHEN item.first_date > '{adate}'::date THEN NULL
        WHEN item.first_date <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE item.id::text
        END, ',' ORDER BY item.id) AS ids_{adate:%Y_%m_%d}
""".format(adate=adate)

def canceledItemCounter(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    count(CASE
        WHEN item.last_date is NULL then NULL
        WHEN item.last_date > '{adate}'::date THEN NULL
        WHEN item.last_date <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE TRUE
        END) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def canceledItemLister(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    string_agg(CASE
        WHEN item.last_date is NULL then NULL
        WHEN item.last_date > '{adate}'::date THEN NULL
        WHEN item.last_date <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE item.id::text
        END, ',' ORDER BY item.id) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def newSelfConsumptionContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeQuery(
        dates=dates,
        queryfile='contract_selfconsumption_distribution',
        timeSlicer=newItemCounter,
        dbhandler=dbhandler,
    )

def canceledSelfConsumptionContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeQuery(
        dates=dates,
        queryfile='contract_selfconsumption_distribution',
        timeSlicer=canceledItemCounter,
        dbhandler=dbhandler,
    )

def selfConsumptionContractsSeries(dates, dbhandler=csvTable, debug=False):
    return timeQuery(
        dates=dates,
        queryfile='contract_selfconsumption_distribution',
        timeSlicer=activeItemCounter,
        dbhandler=dbhandler,
    )

def activeMembersCounter(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    count(CASE
        WHEN create_date IS NULL THEN NULL
        WHEN create_date > '{adate}'::date THEN NULL
        WHEN data_baixa_soci < '{adate}'::date THEN NULL
        WHEN create_date <= '{adate}'::date THEN TRUE
        WHEN active THEN TRUE
        ELSE NULL
            END) AS count_{adate:%Y_%m_%d}
        """.format(adate=adate)

def activeMembersLister(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    string_agg(CASE
        WHEN create_date IS NULL THEN NULL
        WHEN create_date > '{adate}'::date THEN NULL
        WHEN data_baixa_soci < '{adate}'::date THEN NULL
        WHEN create_date <= '{adate}'::date THEN soci_id::text
        WHEN active THEN soci_id::text
        ELSE NULL
        END, ',' ORDER BY soci_id) AS count_{adate:%Y_%m_%d}
        """.format(adate=adate)

def membersSeries(dates, dbhandler=csvTable, debug=False):
    return timeQuery(
        dates=dates,
        queryfile='members_distribution',
        timeSlicer=activeMembersCounter,
        #timeSlicer=activeMembersLister, # debug
        dbhandler=dbhandler,
    )

def newMembersCounter(adate):
    # TODO: Unsafe substitution
    return """
    count(CASE
        WHEN create_date IS NULL THEN NULL
        WHEN create_date > '{adate}'::date THEN NULL
        WHEN create_date <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE TRUE
            END) AS count_{adate:%Y_%m_%d}
        """.format(adate=adate)

def newMembersLister(adate):
    # TODO: Unsafe substitution
    return """
    string_agg(CASE
        WHEN create_date IS NULL THEN NULL
        WHEN create_date > '{adate}'::date THEN NULL
        WHEN create_date <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE soci_id::text
            END, ',' ORDER BY soci_id) AS count_{adate:%Y_%m_%d}
        """.format(adate=adate)

def plantProductionCounter(adate):
    # TODO: Unsafe substitution
    return """
    count(CASE
        WHEN time IS NULL THEN NULL
        WHEN time > '{adate}'::date THEN NULL
        WHEN time <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        WHEN time <= '{adate}'::date THEN TRUE
        ELSE NULL
            END) AS count_{adate:%Y_%m_%d}
        """.format(adate=adate)

def newMembersSeries(dates, dbhandler=csvTable, debug=False):
    return timeQuery(
        dates=dates,
        queryfile='members_distribution',
        timeSlicer=newMembersCounter,
        #timeSlicer=newMembersLister, # debug
        dbhandler=dbhandler,
    )

def canceledMembersCounter(adate):
    # TODO: Unsafe substitution
    return """
    count(CASE
        WHEN data_baixa_soci IS NULL THEN NULL
        WHEN data_baixa_soci > '{adate}'::date THEN NULL
        WHEN data_baixa_soci <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE TRUE
            END) AS count_{adate:%Y_%m_%d}
        """.format(adate=adate)

def canceledMembersLister(adate):
    # TODO: Unsafe substitution
    return """
    string_agg(CASE
        WHEN data_baixa_soci IS NULL THEN NULL
        WHEN data_baixa_soci > '{adate}'::date THEN NULL
        WHEN data_baixa_soci <= '{adate}'::date - INTERVAL '1 month' THEN NULL
        ELSE soci_id::text
            END, ',' ORDER BY soci_id) AS count_{adate:%Y_%m_%d}
        """.format(adate=adate)

def canceledMembersSeries(dates, dbhandler=csvTable, debug=False):
    return timeQuery(
        dates=dates,
        queryfile='members_distribution',
        timeSlicer=canceledMembersCounter,
        #timeSlicer=canceledMembersLister, # debug
        dbhandler=dbhandler,
    )


def plantProductionSeries(dates, dbhandler=csvTable, debug=False):
    db = psycopg2.connect(**config.psycopg_plantmonitor)
    print(config.psycopg_plantmonitor)
    query = readQuery('plant_production')
    query = query.format(','.join(
        plantProductionCounter(Date(adate))
        for adate in dates
        ))
    with db.cursor() as cursor :
        cursor.execute(query)
        return dbhandler(cursor)

# vim: et sw=4 ts=4
