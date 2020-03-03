from yamlns import namespace as ns
from future.utils import iteritems

class TemplateSource(object):

    def __init__(self, templates, styles, translations, legend):
        self.templates = templates
        self.styles = styles
        self.translations = translations
        self.legend = legend

    def getRawTemplate(self, geolevel):
        return self.templates[geolevel]

    def getStyle(self, geolevel):
        return self.styles.get(geolevel, '')

    def getLegend(self):
        return self.legend

    def getTemplate(self, geolevel, lang='en'):
        #TODO: change to format_map() with a default that overrides __missing__ 
        result = self.templates[geolevel]
        for en_name, new_name in iteritems(self.translations[lang]):
            result = result.replace('{'+en_name+'}', new_name, 1)
        result = result.replace('{style}', self.styles.get(geolevel,''))
        return result



import os.path
import glob
from pathlib2 import Path


def loadMapData(relativePath='../maps'):
    myPath = os.path.abspath(os.path.dirname(__file__))
    dataPath = os.path.join(myPath, relativePath)
    fileNames = ['template', 'style']
    mapData = ns()
    for name in fileNames:
        mapData[name] = ns()
        for datafile in glob.glob(os.path.join(dataPath, name+'_*.svg')):
            geolevel = os.path.basename(datafile).replace('.svg', '').replace(name+'_', '')
            mapData[name][geolevel] = Path(datafile).read_text(encoding='utf8')

    translations = ns()
    for datafile in glob.glob(os.path.join(dataPath, 'translations/*')):
        lang = os.path.basename(datafile)
        translations[lang] = ns.loads(Path(datafile).read_text(encoding='utf8'))

    legend = Path(dataPath + '/legend.svg').read_text(encoding='utf8')
    return TemplateSource(templates=mapData.template, styles=mapData.style, translations=translations, legend=legend)
