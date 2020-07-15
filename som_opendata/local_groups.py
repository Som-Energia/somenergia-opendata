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
        return lg.alias

    def getLocalGroups(self):
        return [(k, lg.name) for k, lg in self.data.items()]

#TODO: obtenir la llista de (level, codi) de filtres que el conformen
#TODO: quan tinguem el resultat del aggregate () -> sumar i canviar el nom del
#TODO: llista de grups locals: codi: nom

    def aggregateAlias(self, code, hierarchicalData):
        lgs = self.lgComputeValues(code, hierarchicalData)
        return self.lgHierarchicalResponse(lgs, hierarchicalData)

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

    # def replaceHierarchy(self, hierarchy, level, targetlevel, replacement):
    #     geolevels = [
    #         ('country', 'countries'),
    #         ('ccaa', 'ccaas'),
    #         ('state', 'states'),
    #         ('city', 'cities'),
    #     ]
    #
    #     if level >= len(geolevels):
    #         return
    #
    #     singular, plural = geolevels[level]
    #
    #     for code, region in hierarchy[plural].items():
    #         if plural != code:
    #             self.replaceHierarchy(region, level + 1, targetlevel, replacement)
    #         else:
    #             hierarchy[plural] = replacement

    def lgHierarchicalResponse(self, lgs, hierarchicalData):
        # rebuild minimum common hierarchy
        # place the localgroups in the appropiate place in the hierarchy

        # Approach 0 return localgroups directly
        return lgs

        # Approach 1 rebuild hierarchy from scratch
        # r = ns()
        # r['dates']     = hierarchicalData['dates']
        # r['values']    = hierarchicalData['values']
        # hcountry = hierarchicalData['country']
        # country = ns()
        # country['ES'] =
        # r['countries'] = country
        # response = hierarchicalData

        # Approach 2 replace at hierarchy
        # #deepcopy
        # lg_r = ns.loads(hierarchicalData.dump())
        #
        # for ccaa, ccaa_data in lg_r.countries['ES'].ccaas.items():
        #     ccaa_data['localgroups'] = lgs
        #     del ccaa_data['states']

        # Approach 3 guess hierarchy and replace
        # for lg_pack in lgs:
        #     for lg_code, lg in lg_pack.items():
        #         print(lg_code)
        #         lg_info = self.data[int(lg_code)]
        #         target_level = lg_info.geolevel
        #         self.replaceHierarchy(lg_r, 0, target_level, lg)

        return lg_r

def loadYamlLocalGroups(relativeFile='../data/alias/gl.yaml'):
    myPath = os.path.abspath(os.path.dirname(__file__))
    dataFile = os.path.join(myPath, relativeFile)
    content = ns.load(dataFile)
    return LocalGroups(content)
