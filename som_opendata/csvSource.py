# -*- coding: utf-8 -*-
from yamlns import namespace as ns
from dbutils import csvTable
from distribution import (
    parse_tsv,
    tuples2objects,
    )



# import io

# with io.open('som_opendata/utils/membersSparse_many-expected') as f:
#     data = f.read()


headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"

data = u'\n'.join([
            headers,
            data_Girona,
            data_SantJoan,
        ])

class CsvSource():
    
    def __init__(self, content):
        pass

    def extract(self, field, dates):
        pass





class DataFromCSV():

    def __init__(self):
        return None

    def eliminateIrrelevantDates(self, dataWithDates, dates):

        headersPerEliminar = [
            index for index, value in enumerate(dataWithDates[0]) 
            if 'count' in value and not any([value == 'count_'+date.replace('-','_') for date in dates])
        ]

        return [
            [element for index, element in enumerate(l) if index not in headersPerEliminar]
            for l in dataWithDates
        ]

    #TODO: Cal buscar diferents csv en funcio de 'object'
    def extractObjects(self, object, dates):

        res = parse_tsv(data)

        dataImportant = self.eliminateIrrelevantDates(res,dates)

        if len(dataImportant[0]) <= 8:
            return []
        else:
            return dataImportant

''' TODO: Casos:
    - Nomes hi ha una data i l'usari la vol:        OK
    - Hi ha més d'una data i l'usuari en vol una:   Es filtra
    - Hi ha una data per l'usuari en vol més d'una: Es don només una data 
                                                    i es va a buscar l'altre (?)
    - No hi ha la data:                             Es va a buscar

'''