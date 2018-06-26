from functools import wraps

from flask import Blueprint, request, current_app
from yamlns import namespace as ns

from ..common import yaml_response


modul_socis = Blueprint(name='modul_socis', import_name=__name__)


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


@modul_socis.route('/<country:pais>')
@yaml_response
def socis_pais(pais):
    query = current_app.db.query(
        query_add_countryId_code(), country_code=pais
    ).first()
    return dict(socis=query.count)


@modul_socis.route('/<country:pais>/<int:ccaa>')
@yaml_response
def socis_CCAA(pais, ccaa):
    query = current_app.db.query(
        query_add_ccaaId_code(),
        country_code=pais,
        ccaa_code=ccaa
    ).first()
    return dict(socis=query.count)


@modul_socis.route('/<country:pais>/<int:ccaa>/<int:provincia>')
@yaml_response
def socis_provincia(pais, ccaa, provincia):
    query = current_app.db.query(
        query_add_provinciaId_code(),
        country_code=pais,
        ccaa_code=ccaa,
        provincia_code='{:>02}'.format(str(provincia))
    ).first()
    return dict(socis=query.count)


@modul_socis.route('/<country:pais>/<int:ccaa>/<int:provincia>/<int:ine>')
@yaml_response
def socis_municipi(pais, ccaa, provincia, ine):
    query = current_app.db.query(
        query_add_municipiId_ine(),
        country_code=pais,
        ccaa_code=ccaa,
        provincia_code='{:>02}'.format(str(provincia)),
        ine=str(ine)
    ).first()
    return dict(socis=query.count)
