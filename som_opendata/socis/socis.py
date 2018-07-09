from functools import wraps
from flask import Blueprint, request, current_app, abort
from yamlns import namespace as ns

from ..common import yaml_response


modul_socis = Blueprint(name='modul_socis', import_name=__name__)


def existeix_pais(pais):
    query = current_app.db.query(
        'SELECT count(*) FROM res_country WHERE code LIKE :country_code',
        country_code=pais
    ).first()
    return query.count == 1


def existeix_ccaa(ccaa):
    query = current_app.db.query(
        'SELECT count(*) FROM res_country_state WHERE comunitat_autonoma=:ccaa',
        ccaa=ccaa
    ).first()
    return query.count >= 1


def existeix_provincia(provincia):
    query = current_app.db.query(
        'SELECT count(*) FROM res_country_state WHERE code LIKE :prov',
        prov='{:>02}'.format(str(provincia))
    ).first()
    return query.count == 1


def existeix_municipi(ine):
    query = current_app.db.query(
        'SELECT count(*) FROM res_municipi WHERE ine LIKE :ine',
        ine=str(ine)
    ).first()
    return query.count == 1


def query_select_partner():
    return 'SELECT count(*) FROM res_partner_address'


def query_add_countryId_code():
    return 'SELECT count(*) FROM ' \
           'res_partner_address address, res_country country ' \
           'WHERE address.country_id = country.id ' \
           'AND country.code LIKE :country_code'


def query_add_ccaaId_code():
    return 'SELECT count(*) FROM ' \
           'res_partner_address address, res_country country, res_country_state state ' \
           'WHERE address.country_id = country.id ' \
           'AND address.state_id = state.id ' \
           'AND country.code LIKE :country_code ' \
           'AND state.comunitat_autonoma=:ccaa_code'


def query_add_provinciaId_code():
    return 'SELECT count(*) FROM ' \
           'res_partner_address address, res_country country ' \
           'WHERE address.country_id = country.id ' \
           'AND country.code LIKE :country_code ' \
           'AND state_id in ((select id from res_country_state ' \
           'WHERE comunitat_autonoma=:ccaa_code)) ' \
           'AND state_id = (select id from res_country_state ' \
           'WHERE code like :provincia_code)'


def query_add_municipiId_ine():
    return 'SELECT count(*) FROM ' \
           'res_partner_address address, res_country country ' \
           'WHERE address.country_id = country.id ' \
           'AND country.code LIKE :country_code ' \
           'AND state_id in ((select id from res_country_state ' \
           'WHERE comunitat_autonoma=:ccaa_code)) ' \
           'AND state_id = (select id from res_country_state ' \
           'WHERE code like :provincia_code) ' \
           'AND id_municipi = (select id from res_municipi ' \
           'WHERE ine like :ine)'


def valida_pais(pais):
    return len(pais) == 2


def valida_ccaa(ccaa):
    return ccaa < 20 and ccaa > 0


def valida_provincia(provincia):
    return provincia < 53 and provincia > 0


def valida_ine(ine):
    return len(str(ine)) == 5 and ine > 0


@modul_socis.route('')
@yaml_response
def socis_totals():
    query = current_app.db.query(query_select_partner()).first()

    return dict(socis=query.count)



"""
@api {get} /socis/<country:pais>
@apiVersion 1.0.1
@apiName Socis-Country
@apiGroup Socis
@apiDescription Retorna els socis que hi ha en el pais

@apiSampleRequest http://DNS-NAME:5001/socis/ES
@apiSuccessExample {yaml} Success-Response:
    HTTP/1.1 200OK
    {
        socis: 88000
    }
"""

@modul_socis.route('/<country:pais>')
@yaml_response
def socis_pais(pais):

    if existeix_pais(pais):
        query = current_app.db.query(
            query_add_countryId_code(), country_code=pais
        ).first()
        return dict(socis=query.count)
    else:
        #raise werkzeug.exceptions.BadRequest([pais])
        current_app.e = [pais]
        abort(400)


"""
@api {get} /socis/<country:pais>/<int:ccaa>
@apiVersion 1.0.1
@apiName Socis-CCAA
@apiGroup Socis
@apiDescription Retorna els socis que hi ha en una CCAA d'un pais

@apiSampleRequest http://DNS-NAME:5001/socis/ES/09
@apiSuccessExample {yaml} Success-Response:
    HTTP/1.1 200OK
    {
        socis: 8800
    }
"""

@modul_socis.route('/<country:pais>/<int:ccaa>')
@yaml_response
def socis_CCAA(pais, ccaa):

    errors = make_errors(pais, ccaa)

    if len(errors) == 0:
        query = current_app.db.query(
            query_add_ccaaId_code(),
            country_code=pais,
            ccaa_code=ccaa
        ).first()
        return dict(socis=query.count)
    else:
        current_app.errors = errors
        abort(400)


"""
@api {get} /socis/<country:pais>/<int:ccaa>/<int:provincia>
@apiVersion 1.0.1
@apiName Socis-CCAA
@apiGroup Socis
@apiDescription Retorna els socis que hi ha en una provincia d'una CCAA d'un pais

@apiSampleRequest http://DNS-NAME:5001/socis/ES/09/17
@apiSuccessExample {yaml} Success-Response:
    HTTP/1.1 200OK
    {
        socis: 880
    }
"""

@modul_socis.route('/<country:pais>/<int:ccaa>/<int:provincia>')
@yaml_response
def socis_provincia(pais, ccaa, provincia):

    errors = make_errors(pais, ccaa, provincia)

    if len(errors) == 0:
        query = current_app.db.query(
            query_add_provinciaId_code(),
            country_code=pais,
            ccaa_code=ccaa,
            provincia_code='{:>02}'.format(str(provincia))
        ).first()
        return dict(socis=query.count)
    else:
        current_app.errors = errors
        abort(400)



"""
@api {get} /socis/<country:pais>/<int:ccaa>/<int:provincia>/<int:ine>
@apiVersion 1.0.1
@apiName Socis-CCAA
@apiGroup Socis
@apiDescription Retorna els socis que hi ha en un municipi d'una provincia d'una CCAA d'un pais

@apiSampleRequest http://DNS-NAME:5001/socis/ES/09/17/17079
@apiSuccessExample {yaml} Success-Response:
    HTTP/1.1 200OK
    {
        socis: 88
    }
"""

@modul_socis.route('/<country:pais>/<int:ccaa>/<int:provincia>/<int:ine>')
@yaml_response
def socis_municipi(pais, ccaa, provincia, ine):

    errors = make_errors(pais, ccaa, provincia, ine)

    if len(errors) == 0:
        query = current_app.db.query(
            query_add_municipiId_ine(),
            country_code=pais,
            ccaa_code=ccaa,
            provincia_code='{:>02}'.format(str(provincia)),
            ine=str(ine)
        ).first()
        return dict(socis=query.count)
    else:
        current_app.errors = errors
        abort(400)


def make_errors(pais=None, ccaa=None, provincia=None, ine=None):
    errors = []
    if pais != None and not existeix_pais(pais):
        errors.append(pais)
    if ccaa != None and not existeix_ccaa(ccaa):
        errors.append(ccaa)
    if provincia != None and not existeix_provincia(provincia):
        errors.append(provincia)
    if ine != None and not existeix_municipi(ine):
        errors.append(ine)
    return errors
