
from flask import (
    Blueprint,
    Flask,
    make_response,
    Response,
    )

import logging
from yamlns import namespace as ns
from functools import wraps
import os
import psycopg2
import dbconfig as config
from dbutils import csvTable
from common import yaml_response
from socis.socis import modul_socis


VERSION = 4



old_modul = Blueprint(name='old_modul', import_name=__name__)

sentry = None

def sentry_exception():
    if not sentry: return
    sentry.client.captureException()

def handle(e, status_code):
    response = make_response(ns(
        error=type(e).__name__,
        message=str(e),
        arguments=e.arguments if hasattr(e,'arguments') else []
        ).dump())
    response.mimetype='application/yaml'
    response.status_code = status_code
    return response


def utf8(thing):
    if type(thing) is unicode: return thing
    if type(thing) is str: return unicode(thing,'utf-8',errors='ignore')
    return unicode(thing)

def tsv_response(f):
    @wraps(f)
    def wrapper(*args, **kwd):
        result = f(*args, **kwd)

        if type(result) is Response:
            return result
        if type(result) in (str,unicode):
            response = make_response(result)
            response.mimetype='text/tab-separated-values'
            response.headers["Content-Disposition"] = "filename=contracts.tsv"
            return response

        response = make_response('\n'.join(
            '\t'.join(
                utf8(x)
                    .replace('\t',' ')
                    .replace('\n',' ')
                for x in line)
            for line in result
        ))
        response.mimetype='text/tab-separated-values'
        response.charset='utf-8'
        response.headers["Content-Disposition"] = "attachment; filename=myplot.tsv"
        return response
    return wrapper


from yamlns.dateutils import Date

from .common import (
    dateSequence,
    readQuery,
    )

def activeContractCounter(adate):
    # TODO: Unsafe substitution
    return """
	count(CASE
		WHEN polissa.data_alta IS NULL THEN NULL
		WHEN polissa.data_alta > '{adate}'::date THEN NULL
		WHEN polissa.data_baixa is NULL then TRUE
		WHEN polissa.data_baixa > '{adate}'::date THEN TRUE
		ELSE NULL
		END) AS count_{adate:%Y_%m_%d}
""".format(adate=adate)

def activeContractLister(adate):
    # TODO: Unsafe substitution
    return """
	string_agg(CASE
		WHEN polissa.data_alta IS NULL THEN NULL
		WHEN polissa.data_alta > '{adate}'::date THEN NULL
		WHEN polissa.data_baixa is NULL then polissa.id::text
		WHEN polissa.data_baixa > '{adate)s'::date THEN polissa.id::text
		ELSE NULL
		END, ',' ORDER BY polissa.id) AS ids_{adate},
""".format(adate=adate)


def contractsSparse(dates):
    db = psycopg2.connect(**config.psycopg)
    query = readQuery('contract_distribution_sparse')
    with db.cursor() as cursor :
        cursor.execute(query, dict(dates=[
            [Date(adate) for adate in dates]
        ]))
        return csvTable(cursor)

def contractsSeries(dates):
    db = psycopg2.connect(**config.psycopg)
    query = readQuery('contract_distribution')
    query = query.format(','.join(
        activeContractCounter(Date(adate))
        for adate in dates
        ))
    with db.cursor() as cursor :
        cursor.execute(query)
        return csvTable(cursor)

subquerySocis = """\
SELECT
    pc.name AS categoria,
    m.name AS municipi,
    p.ref AS num_soci,
    p.vat AS nif,
    pa.email AS email,
    pa.name AS nom,
    prov.name AS provincia,
    pa.zip AS codi_postal,
    p.lang AS idioma,
    com.name AS comarca,
    ccaa.name AS comunitat_autonoma,
    country.name AS pais,
    pa.id AS soci_id,
    m.id AS id_municipi,
    m.ine AS codi_ine,
    prov.code AS codi_provincia,
    ccaa.codi AS codi_ccaa,
    country.code AS codi_pais,
    dades_inicials.partner_id AS partner_id
FROM res_partner_address AS pa
JOIN (
    SELECT
        dades_inicials.partner_id,
        MIN(dades_inicials.id) AS id_unic
    FROM
        res_partner_address as dades_inicials
    WHERE
        dades_inicials.active
    GROUP BY dades_inicials.partner_id
    ) AS dades_inicials ON dades_inicials.id_unic = pa.id
LEFT JOIN res_partner AS p ON (p.id=pa.partner_id)
LEFT JOIN res_partner_category_rel AS p__c ON (pa.partner_id=p__c.partner_id)
LEFT JOIN res_partner_category AS pc ON (pc.id=p__c.category_id and pc.name='Soci')
LEFT JOIN res_municipi AS m ON (m.id=pa.id_municipi)
LEFT JOIN res_country_state AS prov ON (prov.id=pa.state_id)
LEFT JOIN res_comunitat_autonoma AS ccaa ON (ccaa.id=prov.comunitat_autonoma)
LEFT JOIN res_comarca AS com ON (com.id=m.comarca)
LEFT JOIN res_country AS country ON (country.id=pa.country_id)
WHERE
    pa.active AND
    pa.create_date <= %(date)s AND
    p__c.category_id IS NOT NULL AND
    p__c.category_id = (SELECT id FROM res_partner_category WHERE name='Soci')
ORDER BY p.ref
"""

def membersSparse(dates, dbhandler, debug=False):
    date = dates[0]

    db = psycopg2.connect(**config.psycopg)
    with db.cursor() as cursor :
        cursor.execute("""\
SELECT
    codi_pais,
    pais,
    codi_ccaa,
    comunitat_autonoma,
    codi_provincia,
    provincia,
    codi_ine,
    municipi,
    COUNT(soci_id) AS quants
    """ + ( ", STRING_AGG(num_soci::text, ',' ORDER BY partner_id DESC) AS partners" if debug else "") + """
FROM ("""+subquerySocis+""") AS detall
GROUP BY
    codi_pais,
    codi_ccaa,
    codi_provincia,
    codi_ine,
    pais,
    provincia,
    municipi,
    comunitat_autonoma,
    TRUE
ORDER BY
    pais ASC,
    comunitat_autonoma ASC,
    provincia ASC,
    municipi ASC,
    TRUE ASC
""", dict(
        date=date,
        ))

        return dbhandler(cursor)




@old_modul.route('/version')
@yaml_response
def version():
    return ns(
        version = '1.0',
        )

@old_modul.route('/contracts/<isodate:fromdate>')
@old_modul.route('/contracts/<isodate:fromdate>/monthlyto/<isodate:todate>')
@tsv_response
def contracts(fromdate=None, todate=None):
    dates=dateSequence(fromdate, todate)
    return contractsSeries(dates)

@old_modul.route('/members/<isodate:fromdate>')
@old_modul.route('/members/<isodate:fromdate>/monthlyto/<isodate:todate>')
@tsv_response
def members(fromdate=None, todate=None):
    dates=dateSequence(fromdate, todate)
    return membersSparse([fromdate], csvTable)

