from flask import Response, make_response
from .errors import (
    ValidateError,
)
from consolemsg import u
from yamlns import namespace as ns

implemented = ns(
    metric=['members', 'contracts'],
    geolevel=['ccaa','state'],
    relativemetric=['population', None],
    )


def validateImplementation(data):
    for field, value in data:
        if field != 'frequency':
            if value not in implemented[field]:
                raise ValidateImplementationMap(field=field, value=value)


class ValidateImplementationMap(ValidateError):
    def __init__(self, field, value):
        self.parameter = field
        self.value = value
        self.possibleValues = implemented[field]
        super(ValidateError, self).__init__(
            u"Not implemented {} '{}' try with {}"
            .format(field, value, self.possibleValues))


import os.path
from pathlib2 import Path

def loadMapData(folderName='maps'):
    dataPath = Path('./{}'.format(folderName))
    mapData = ns()
    templateFolder = Path(dataPath / "mapTemplates")
    for datafile in os.listdir(templateFolder):
        geolevel = datafile.replace('.svg','')
        mapData[geolevel] = ns()
        mapData[geolevel].template = Path(templateFolder /'{}'.format(datafile)).read_text(encoding='utf8')
        styleFile = Path(dataPath / 'style_{}.svg'.format(geolevel))
        if styleFile.is_file():
            mapData[geolevel].style = styleFile.read_text(encoding='utf8')
        else:
            mapData[geolevel].style =''
    mapData['legend'] = Path(dataPath/'legend.svg').read_text(encoding='utf8')
    translationsFolder = Path(dataPath/'translations')
    mapData.translations = ns()
    for datafile in os.listdir(translationsFolder):
        mapData.translations[datafile] = ns.loads(Path(translationsFolder /'{}'.format(datafile)).read_text(encoding='utf8'))

    return mapData
