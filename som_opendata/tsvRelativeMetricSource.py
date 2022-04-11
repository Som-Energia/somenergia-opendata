from yamlns import namespace as ns
from .distribution import parse_tsv, tuples2objects
from future.utils import iteritems


class TsvRelativeMetricSource(object):

    def __init__(self, data):
        self.metrics = [metric for metric in data.keys()]
        dataToObjects = ns()
        for metric in self.metrics:
            dataToObjects[metric] = ns()
            for geolevel in data[metric]:
                dataToObjects[metric][geolevel] = \
                    tuples2objects(parse_tsv(data[metric][geolevel]))

        self.values = ns()
        for metric, data in iteritems(dataToObjects):
            self.values[metric] = ns()
            for geolevel, item in iteritems(data):
                self.values[metric][geolevel] = \
                    getFieldBy(
                        field=metric,
                        by='code',
                        data=dataToObjects[metric][geolevel]
                    )
        self.dataObjects = dataToObjects

    def getValuesByCode(self, geolevel, metric='population'):

        self.validateMetricGeolevel(metric=metric, geolevel=geolevel)
        return self.values[metric][geolevel]

    def getDataObjects(self, metric, geolevel):
        return self.dataObjects[metric][geolevel]

    def getCodesByGeolevel(self, geolevel):
        self.validateMetricGeolevel(geolevel=geolevel)
        return list(self.values['population'][geolevel].keys())

    def validateMetricGeolevel(self, geolevel, metric='population'):
        if not self.values.get(metric):
            raise ValueError("Relative metric {} not found".format(metric))
        if not self.values[metric].get(geolevel):
            raise ValueError("Geolevel {} not found for {}".format(geolevel, metric))


def getFieldBy(field, by, data, numeric=True):
    result = ns()
    for item in data:
        value = item[field]
        if numeric:
            value = int(value)
        result.update({item[by]: value})
    return result


import os.path
import glob
from pathlib import Path


def loadTsvRelativeMetric(relativePath='../data/relativeMetrics'):
    myPath = os.path.abspath(os.path.dirname(__file__))
    dataPath = os.path.join(myPath, relativePath)
    relativeMetrics = ns()
    for datafile in glob.glob(os.path.join(dataPath, '*tsv')):
        metric, geolevel = os.path.basename(datafile).replace('.tsv', '').split('_')
        if not relativeMetrics.get(metric):
            relativeMetrics[metric] = ns()
        relativeMetrics[metric][geolevel] = Path(datafile).read_text(encoding='utf8')

    return TsvRelativeMetricSource(relativeMetrics)
