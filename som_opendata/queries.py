import os
import psycopg2
import dbconfig as config
from dbutils import csvTable
from yamlns import namespace as ns
from yamlns.dateutils import Date
from pathlib import Path

"""
This module contains functions to precompute metrics.
Metrics have to be computed aggregated by city and month.

Precomputed metric data results in the following fields:

- `codi_pais`: ISO code of the country
- `codi_ccaa`: INE code of the CCAA
- `codi_provincia`: INE code of the province
- `codi_ine`: INE code of the city
- `pais`: name of the country
- `comunitat_autonoma`: name of the CCAA
- `provincia`: name of the province
- `municipi`: name of the city
- `count_YYYY_MM_DD`: the metric value for the date YYYY-MM-DD in the given geolocation

This module also contains helper functions to build such aggregation
from simpler queries.
"""

def readQuery(query):
    queryfile = Path(__file__).absolute().parent / 'queries' / (query + '.sql')
    return queryfile.read_text(encoding='utf8').rstrip()

def timeQuery(dates, queryfile, timeSlicer, dbhandler=csvTable, dbconfig=None):
    """
    Executes a query stored in queryfile
    extending it with a column for each passed date
    which aggregates rows by that date.

    The timeSlicer parameter tells whether to filter or not
    each row for a given date and how to aggregate it.

    The expected base query returns the following fields:

    - `id`: id of the item taken into account (recommended for debugging, with lister timeSlicer)
    - `value`: value to add when aggregated (only for adder timeslicers)
    - `first_date`: first date the item is taken into account
    - `last_date`: last date the item is taken into account
    - `codi_pais`: ISO code of the country
    - `codi_ccaa`: INE code of the CCAA
    - `codi_provincia`: INE code of the province
    - `codi_ine`: INE code of the city
    - `pais`: name of the country
    - `comunitat_autonoma`: name of the CCAA
    - `provincia`: name of the province
    - `municipi`: name of the city
    """
    dbconfig = dbconfig or config.psycopg
    db = psycopg2.connect(**dbconfig)
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
    aggregating data for each date in `dates` as specified by `timeSlicer`
    and also geographical columns.

    To be used only for querys against the ERP database,
    to simplify obtainig the geographical columns.

    In order to work, the inner query is expected to generate those fields:

    - `id`: id of the item taken into account (recommended for debugging, with lister timeSlicer)
    - `value`: value to add when aggregated (only for adder timeslicers)
    - `first_date`: first date the item is taken into account
    - `last_date`: last date the item is taken into account
    - `city_id`: ERP id of the city
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

"""
Time slicers: Produces date columns. 

Decides whether each item is chosen or not for a given date given its
`first_date` and `last_date` fields and how to perform the aggregation.

This can be used to select items:

- items actives during the period (active),
- items activated during the period (new), or
- items deactivated during the period (canceled).

Depending on how the aggregation is done:

- counter: counts items
- adder: adds the items `value` field
- lister: generates a comma separated list of `id` fields (for debugging)

Counters and listers differ on whether we simply count the items
or produce a comma separated list of case ids.
"""

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

"""
Metric functions
TODO: modularize them along with its metadata and sql
"""

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
        timeSlicer=canceledItemLister if debug else canceledItemCounter,
        dbhandler=dbhandler,
    )

# TODO: Rely in plantmonitor data
def plantPowerSeries(dates, dbhandler=csvTable, debug=False):
    return timeQuery(
        dates=dates,
        queryfile='plantpower',
        timeSlicer=activeItemLister if debug else activeItemAdder,
        dbhandler=dbhandler,
        dbconfig=config.plantmonitor_psycopg, # This is different!
    )

# TODO: Make the query work with standard timeSlicers
def plantProductionAdder(adate):
    # TODO: Unsafe substitution, use mogrify
    return """
    sum(CASE
        WHEN (item.time::date + '1 month'::interval)::date = '{adate}'::date  THEN item.value
        ELSE 0
        END)::integer AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def plantProductionSeries(dates, dbhandler=csvTable):
    return timeQuery(
        dates=dates,
        queryfile='plantproduction',
        timeSlicer=plantProductionAdder,
        dbhandler=dbhandler,
        dbconfig=config.plantmonitor_psycopg, # This is different!
    )

# vim: et sw=4 ts=4
