from yamlns import namespace as ns
import os.path
from .map import iterateLevel

class LocalGroups(object):
    def __init__(self, dump):
        self.geolevel = 'lg'
        self.data = dump

    def aliasFilters(self, code):
        lg = self.data.get(code, None)
        if not lg:
            return None
        return [(lg.geolevel, code) for code in lg.codes]

    def getLocalGroups(self):
        return [(k, lg.name) for k, lg in self.data.items()]

#TODO: obtenir la llista de (level, codi) de filtres que el conformen
#TODO: quan tinguem el resultat del aggregate () -> sumar i canviar el nom del
#TODO: llista de grups locals: codi: nom

    def aggregateAlias(self, code, hierarchicalData):
        lgs = self.lgComputeValues(code, hierarchicalData)
        return self.lgHierarchicalResponse(lgs)

    def lgComputeValues(self, codes, hierarchicalData):

        result = ns()
        for code in codes:
            lg_info = self.data[code]
            level = lg_info.geolevel
            lg = ns(name=lg_info.name,values=[0]*len(hierarchicalData['dates']))
            for level_code, entry in iterateLevel(hierarchicalData, level):
                if level_code in lg_info.codes:
                    lg['values'] = [x + y for x, y in zip(lg['values'], entry['values'])]
            result[code] = lg
        return result

    def lgHierarchicalResponse(self, lgs):
        # rebuild minimum common hierarchy
        # place the localgroups in the appropiate place in the hierarchy
        pass

def loadYamlLocalGroups(relativeFile='../data/alias/gl.yaml'):
    myPath = os.path.abspath(os.path.dirname(__file__))
    dataFile = os.path.join(myPath, relativeFile)
    content = ns.load(dataFile)
    return LocalGroups(content)
