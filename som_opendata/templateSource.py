from yamlns import namespace as ns


class TemplateSource(object):

    def __init__(self, templates, legend):
        self.templates = templates
        self.legend = legend

    def getLegend(self):
        return self.legend

    def getTemplate(self, geolevel, lang='en', filters=dict(country=['ES']), fake=False):
        if fake:
            geolevel = 'dummy'

        def getSingleFilter(filters):
            for level, regions in filters.items():
                for region in regions:
                    return level, region.lower()
            return 'country', 'ES'.lower()

        filterlevel, region = getSingleFilter(filters)

        if (geolevel, filterlevel, region, lang) not in self.templates:
            raise ValueError(
                f"No map template found for {filterlevel}={region}"
                f" detailed by {geolevel} in language '{lang}'")

        return self.templates[geolevel, filterlevel, region, lang]



import os.path
import glob
from pathlib2 import Path


def loadMapData(relativePath='../data/maps'):
    codePath = Path(__file__).parent.absolute()
    dataPath = (codePath / relativePath).resolve()
    templates = ns()
    for datafile in dataPath.glob('mapTemplates/*'):
        geolevel, filtergeolevel, filterregion, lang = datafile.stem.split('_')
        templates[geolevel, filtergeolevel, filterregion, lang] = datafile.read_text(encoding='utf8')

    legend = (dataPath / 'legend.svg').read_text(encoding='utf8')

    return TemplateSource(templates=templates, legend=legend)
