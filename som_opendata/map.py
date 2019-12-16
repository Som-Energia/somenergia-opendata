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

def maxValue(data, geolevel):

    def processLevelMax(parentRegion, level, currentMax):
        singular, plural = geolevels[level]
        for code, region in parentRegion[plural].items():
            if singular != geolevel:
                currentMax = processLevelMax(region, level+1, currentMax)
                continue
            value = region["values"][0]
            if value > currentMax:
                currentMax = value
        return currentMax

    return processLevelMax(data.countries.ES, 0, 0)

def dataToTemplateDict(data, colors, title, subtitle, colorScale='Log', locations=[], geolevel='ccaa', maxValue=None):
    date = data.dates[0]
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
    totalValue = maxValue or data["values"][0]

    scale = scales[colorScale](higher=totalValue or 1)

    def updateDict(code, value):
        result.update({
                'number_' + code: value,
                'percent_' + code: percentRegion(value, totalValue),
                'color_' + code: colors(scale(value)),
                })

    # TODO: just for tests 
    if geolevel == 'dummy':
        geolevel = 'ccaa'

    def processLevel(parentRegion, level):
        singular, plural = geolevels[level]
        for code, region in parentRegion[plural].items():
            if singular != geolevel:
                processLevel(region, level+1)
                continue
            value = region["values"][0]
            updateDict(code, value)

    processLevel(data.countries.ES, 0)

    restWorld = data["values"][0] - data.countries.ES["values"][0]
    updateDict('00',restWorld)

    for code in locations:
        if 'number_{}'.format(code) in result:
            continue
        updateDict(code, 0)
    return result


def fillMap(data, template, geolevel, title, subtitle='', scale='Log', locations=[]):
    gradient = Gradient('#e0ecbb','#384413')
    dataDict = dataToTemplateDict(
        data=data, colors=gradient,
        colorScale=scale, title=title, subtitle=subtitle, locations=locations, geolevel=geolevel
    )

    return template.format(**dataDict)

def renderMap(source, metric, date, geolevel):
    locationContent = Path('maps/population_{}.tsv'.format(geolevel)).read_text(encoding='utf8')
    locations = [
        location.code for location in tuples2objects(parse_tsv(locationContent))
    ]
    filtered_objects = source.get(metric, date, [])
    data = aggregate(filtered_objects, geolevel)
    template = Path('maps/mapTemplate_{}.svg'.format(geolevel)).read_text(encoding='utf8')
    return fillMap(data=data, template=template, title=metric.title(), locations=locations, geolevel=geolevel)


# map{Country}{ES}by{States}.svg
# map{Province}{01}by{Counties}.svg

# map.templateName(scope, code, subscope)
# map.subdivisions(scope, code, subscope)
