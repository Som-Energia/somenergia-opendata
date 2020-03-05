from yamlns import namespace as ns
from .distribution import parse_tsv, tuples2objects
from future.utils import iteritems

class TsvRelativeMetricSource(object):

    def __init__(self, data):
        self.metrics = [metric for metric in data.keys()]
        dataToObjects= ns()
        for metric in self.metrics:
            dataToObjects[metric] = ns()
            for geolevel in data[metric]:
                dataToObjects[metric][geolevel]= tuples2objects(parse_tsv(data[metric][geolevel]))

        self.names = ns()
        for metric, data in iteritems(dataToObjects):
            self.names[metric]=ns()
            for geolevel, item in iteritems(data):
                self.names[metric][geolevel] = getFieldBy(data=dataToObjects[metric][geolevel], field='name', by='code')

    def getNamesByCode(self, metric, geolevel):
        return self.names[metric][geolevel]


import os.path
import glob
from pathlib2 import Path

def getFieldBy(field, by, data):
    result = ns()
    for item in data:
        result.update({item[by]: item[field]})
    return result


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
