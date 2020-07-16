from yamlns import namespace as ns
import os.path
from .map import iterateLevel
from .errors import AliasNotFoundError

class LocalGroups(object):
    def __init__(self, dump):
        self.alias = 'lg'
        self.data = dump

    def get(self, code):
        try:
            return self.data[code].deepcopy()
        except:
            raise AliasNotFoundError('localgroup', code)

    def aliasFilters(self, codes):
        result = ns()
        for code in codes:
            lg = self.get(code)
            for key, value in lg.alias.items():
                if result.get(key, False):
                    result[key] += value
                else:
                    result[key] = value
        return result

    def getLocalGroups(self):
        return [(k, lg.name) for k, lg in self.data.items()]


def loadYamlLocalGroups(relativeFile='../data/alias/gl.yaml'):
    myPath = os.path.abspath(os.path.dirname(__file__))
    dataFile = os.path.join(myPath, relativeFile)
    content = ns.load(dataFile)
    return LocalGroups(content)
