from yamlns import namespace as ns
from .distribution import parse_tsv, tuples2objects
from future.utils import iteritems

class TsvRelativeMetricSource(object):
    pass

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
