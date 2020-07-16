from yamlns import namespace as ns
import os.path
from .map import iterateLevel
from .errors import AliasNotFoundError

class LocalGroups(object):
    def __init__(self, dump):
        self.geolevel = 'lg'
        self.data = dump

    def get(self, code):
        try:
            return self.data[code].deepcopy()
        except:
            raise AliasNotFoundError('localgroup', code)

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



def loadYamlLocalGroups(relativeFile='../data/alias/gl.yaml'):
    myPath = os.path.abspath(os.path.dirname(__file__))
    dataFile = os.path.join(myPath, relativeFile)
    content = ns.load(dataFile)
    return LocalGroups(content)
