from functools import wraps

import psycopg2
from flask import Blueprint
from yamlns import namespace as ns

import dbconfig as config
from ..common import yaml_response


modul_socis = Blueprint(name='modul_socis', import_name=__name__)

def query_select_partner():
    return 'SELECT count(*) FROM res_partner_address'


def query_add_countryId_code(county_code):
    return 'country_id=(select id from res_country where code like \''+county_code+'\')'


def query_add_ccaaId_code(ccaa_code):
    return 'state_id in ((select id from res_country_state where comunitat_autonoma=\''+ccaa_code+'\'))'

def query_add_provinciaId_code(provincia_code):
    return 'state_id = (select id from res_country_state where code like \''+provincia_code+'\')'

def query_add_municipiId_ine(ine):
    return 'id_municipi = (select id from res_municipi where ine like \''+ine+'\')'


@modul_socis.route('/')
@yaml_response
def socis_totals():
    #print(request.args.get('clau',''))
    db = psycopg2.connect(**config.psycopg)
    with db.cursor() as cursor :
        cursor.execute(query_select_partner())
        result = cursor.fetchone()
        return dict(socis=result[0])


@modul_socis.route('/<pais>')
@yaml_response
def socis_pais(pais):
    db = psycopg2.connect(**config.psycopg)
    with db.cursor() as cursor :
        cursor.execute(query_select_partner()+' WHERE '+query_add_countryId_code(pais))
        result = cursor.fetchone()
        return dict(pais=pais, socis=result[0])


@modul_socis.route('/<pais>/<ccaa>')
@yaml_response
def socis_CCAA(pais, ccaa):
    db = psycopg2.connect(**config.psycopg)
    with db.cursor() as cursor :
        cursor.execute(query_select_partner()+' WHERE '+query_add_countryId_code(pais) + 
            ' AND '+query_add_ccaaId_code(ccaa))
        result = cursor.fetchone()
        return dict(pais=pais, socis=result[0])


@modul_socis.route('/<pais>/<ccaa>/<provincia>')
@yaml_response
def socis_provincia(pais, ccaa, provincia):
    db = psycopg2.connect(**config.psycopg)
    with db.cursor() as cursor :
        cursor.execute(query_select_partner()+' WHERE '+query_add_countryId_code(pais) + 
            ' AND '+query_add_ccaaId_code(ccaa)+' AND '+query_add_provinciaId_code(provincia))
        result = cursor.fetchone()
        return dict(pais=pais, socis=result[0])


@modul_socis.route('/<pais>/<ccaa>/<provincia>/<ine>')
@yaml_response
def socis_municipi(pais, ccaa, provincia, ine):
    db = psycopg2.connect(**config.psycopg)
    with db.cursor() as cursor :
        cursor.execute(query_select_partner()+' WHERE '+query_add_countryId_code(pais) + 
            ' AND '+query_add_ccaaId_code(ccaa)+' AND '+query_add_provinciaId_code(provincia) +
            ' AND '+query_add_municipiId_ine(ine))
        result = cursor.fetchone()
        return dict(pais=pais, socis=result[0])