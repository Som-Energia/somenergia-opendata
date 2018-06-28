# -*- coding: utf-8 -*-
from yamlns import namespace as ns

def parse_tsv(tsv_data):
    return [
        [item.strip() for item in line.split('\t')]
        for line in tsv_data.split('\n')
        if line.strip()
        ]


def tuples2objects(tuples):
    return ns(name='value')


# @old_modul.route('/members/aux')
# def members_2_rows():
#     with open('../random/csv_allColums_2Rows') as f:
#         data = f.readlines()
#     ln1 = [d.replace('\t', ' ').replace('\n', '') for d in data]
#     headers = ln1[0].split()
#     ln1.remove(ln1[0])
#     ln1 = [d.replace('\t', ' ').replace('\n', '').split() for d in ln1]
#     aux = [ns(zip(headers, n)) for n in ln1]
#     return aux



# vim: et sw=4 ts=4