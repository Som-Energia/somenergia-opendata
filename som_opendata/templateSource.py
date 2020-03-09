from yamlns import namespace as ns


class TemplateSource(object):

    def __init__(self, templates, legend):
        self.templates = templates
        self.legend = legend

    def getLegend(self):
        return self.legend

    def getTemplate(self, geolevel, lang='en', fake=False):
        if fake:
            geolevel = 'dummy'
        if geolevel not in self.templates.keys():
            raise ValueError("Template for geolevel {} not found".format(geolevel))

        if lang not in self.templates[geolevel].keys():
            raise ValueError("Template in {} not found".format(lang))

        return self.templates[geolevel][lang]



import os.path
import glob
from pathlib2 import Path


def loadMapData(relativePath='../data/maps'):
    myPath = os.path.abspath(os.path.dirname(__file__))
    dataPath = os.path.join(myPath, relativePath)
    templates = ns()
    for datafile in glob.glob(os.path.join(dataPath, 'mapTemplates/*')):
        geolevel, lang = os.path.basename(datafile).split('_')
        if not templates.get(geolevel):
            templates[geolevel]= ns()
        templates[geolevel][lang] = Path(datafile).read_text(encoding='utf8')

    legend = Path(dataPath + '/legend.svg').read_text(encoding='utf8')

    return TemplateSource(templates=templates, legend=legend)
