from yamlns import namespace as ns

class TemplateSource(object):

    def __init__(self, templates):
        self.templates = templates

    def getTemplate(self, geolevel):
        return self.templates[geolevel]


import os.path
import glob
from pathlib2 import Path


def loadMapData(relativePath='../maps'):
    myPath = os.path.abspath(os.path.dirname(__file__))
    dataPath = os.path.join(myPath, relativePath)
    mapTemplates = ns()
    for datafile in glob.glob(os.path.join(dataPath, 'mapTemplate_*.svg')):
        geolevel = os.path.basename(datafile).replace('.svg','').replace('mapTemplate_', '')
        mapTemplates[geolevel] = Path(datafile).read_text(encoding='utf8')

    return TemplateSource(mapTemplates)
