from yamlns import namespace as ns

class TemplateSource(object):

    def __init__(self, templates, styles, translations, legend):
        self.templates = templates
        self.styles = styles
        self.translations = translations
        self.legend = legend

    def getTemplate(self, geolevel):
        return self.templates[geolevel]

    def getStyle(self, geolevel):
        return self.styles.get(geolevel, '')

    def getLegend(self):
        return self.legend


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

    mapStyles = ns()
    for datafile in glob.glob(os.path.join(dataPath, 'style_*.svg')):
        geolevel = os.path.basename(datafile).replace('.svg','').replace('style_', '')
        mapStyles[geolevel] = Path(datafile).read_text(encoding='utf8')

    translations = ns()
    for datafile in glob.glob(os.path.join(dataPath, 'translations/*')):
        lang = os.path.basename(datafile)
        translations[lang] = ns.loads(Path(datafile).read_text(encoding='utf8'))

    legend = Path(dataPath+'/legend.svg').read_text(encoding='utf8')
    return TemplateSource(templates=mapTemplates, styles=mapStyles, translations=translations, legend=legend)
