from yamlns import namespace as ns
from .scale import LinearScale, LogScale
from .colorscale import Gradient
from .distribution import aggregate, parse_tsv, tuples2objects
from pathlib2 import Path


months = (
        "Enero Febrero Marzo Abril Mayo Junio "
        "Julio Agosto Septiembre Octubre Noviembre Diciembre"
        ).split()


geolevels=[
    ('ccaa', 'ccaas'),
    ('state','states'),
    ('city', 'cities'),
    ]
def percentRegion(value, total):
    if not total:
        return '0,0%'
    return '{:.1f}%'.format(value * 100. / total).replace('.',',')

def maxValue(data, geolevel, frame):

    def processLevelMax(parentRegion, level, currentMax, frame):
        singular, plural = geolevels[level]
        for code, region in parentRegion[plural].items():
            if singular != geolevel:
                currentMax = processLevelMax(region, level+1, currentMax, frame)
                continue
            value = region["values"][frame]
            if value > currentMax:
                currentMax = value
        return currentMax

    return processLevelMax(data.countries.ES, 0, 0, frame)


def iterateLevel(data, geolevel):
    geolevels = [
        ('ccaa', 'ccaas'),
        ('state', 'states'),
        ('city', 'cities'),
    ]

    def processLevel(parentRegion, level):
        singular, plural = geolevels[level]
        for code, region in parentRegion[plural].items():
            if singular != geolevel:
                yield from processLevel(region, level + 1)
                continue
            yield code, region

    yield from processLevel(data.countries.ES, 0)



def dataToTemplateDict(data, colors, title, subtitle, colorScale='Log', locations=[], geolevel='ccaa', maxVal=None, frame=0):
    date = data.dates[frame]
    result = ns(
            title = title,
            subtitle = subtitle,
            year = date.year,
            month = months[date.month-1],
        )

    scales = dict(
        Linear = LinearScale,
        Log = LogScale,
    )

    # TODO: just for tests
    if geolevel == 'dummy':
        geolevel = 'ccaa'

    totalValue = data["values"][frame]
    maxColor = maxVal or maxValue(data, geolevel, frame)

    scale = scales[colorScale](higher=maxColor or 1)

    def updateDict(code, value):
        result.update({
                'number_' + code: value,
                'percent_' + code: percentRegion(value, totalValue),
                'color_' + code: colors(scale(value)),
                })

    for code, region in iterateLevel(data, geolevel):
        updateDict(code, region["values"][frame])

    restWorld = data["values"][frame] - data.countries.ES["values"][frame]
    updateDict('00',restWorld)

    for code in locations:
        if 'number_{}'.format(code) in result:
            continue
        updateDict(code, 0)
    return result


def fillMap(data, template, geolevel, title, subtitle='', scale='Log', locations=[], maxVal=None):
    gradient = Gradient('#e0ecbb', '#384413')
    dataDict = dataToTemplateDict(
        data=data, colors=gradient,
        colorScale=scale, title=title, subtitle=subtitle, locations=locations, geolevel=geolevel, maxVal=maxVal
    )

    return template.format(**dataDict)


def toPopulationRelative(data, geolevel, population):

    def processLevelPopulation(parentRegion, level, frame):
        singular, plural = geolevels[level]
        for code, region in parentRegion[plural].items():
            if singular != geolevel:
                processLevelPopulation(region, level+1, frame)
                continue
            region["values"][frame] = region["values"][frame]*10000 / populationDict[code]

    populationDict = dict()
    for location in population:
        populationDict.update({location.code: int(location.population)})

    for index in range(len(data.dates)):
        processLevelPopulation(data.countries.ES, 0, index)


def renderMap(source, metric, date, geolevel):
    locationContent = Path('maps/population_{}.tsv'.format(geolevel)).read_text(encoding='utf8')
    populationPerLocation = tuples2objects(parse_tsv(locationContent))

    locations = [
        location.code for location in populationPerLocation
    ]

    filtered_objects = source.get(metric, date, [])
    data = aggregate(filtered_objects, geolevel)
    template = Path('maps/mapTemplate_{}.svg'.format(geolevel)).read_text(encoding='utf8')
    return fillMap(data=data, template=template, title=metric.title(), locations=locations, geolevel=geolevel)


# map{Country}{ES}by{States}.svg
# map{Province}{01}by{Counties}.svg

# map.templateName(scope, code, subscope)
# map.subdivisions(scope, code, subscope)
