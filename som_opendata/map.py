from __future__ import division
from yamlns import namespace as ns
from .scale import LinearScale, LogScale
from .colorscale import Gradient
from .distribution import aggregate, parse_tsv, tuples2objects
from pathlib2 import Path
from math import log10, floor
from flask_babel import _

months = ["January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"]

def percentRegion(value, total):
    if not total:
        return '0,0%'
    return '{:.1f}%'.format(value * 100. / total).replace('.',',')

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
                for l in processLevel(region, level + 1):
                    yield l
                continue
            yield code, region

    for l in processLevel(data.countries.ES, 0):
        yield l

def maxValue(data, geolevel, frame):

    currentMax = 0
    for code, region in iterateLevel(data, geolevel):
        value = region["values"][frame]
        if value > currentMax:
            currentMax = value

    return currentMax


def fillLegend(legendTemplate, scale, colors, isRelative):
    result = dict()
    for num in [0, 25, 50, 75, 100]:
        value = int(scale.inverse(num / 100))
        if not isRelative:
            value = int(round(value, -1))
        if isRelative and (num == 25 or num == 75):
            value = ''
        result.update({
            'legendNumber_{}'.format(num): value,
            'legendColor_{}'.format(num): colors(num / 100)
        })

    return legendTemplate.format(**result)


def dataToTemplateDict(data, colors, scale, title, subtitle,
        locations=[], geolevel='ccaa', frame=0, isRelative=False):
    date = data.dates[frame]
    result = ns(
            title = _(title),
            subtitle = subtitle,
            year = date.year,
            month = _(months[date.month-1]),
        )

    totalValue = data["values"][frame]

    def updateDict(code, value):
        if (isRelative):
            result.update({
                'number_' + code: '{:.1f}'.format(value).replace('.',','),
                'percent_' + code: '',
                'color_' + code: colors(scale(value)),
                })
        else:
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


def fillMap(data, template, legendTemplate, geolevel, title,
        subtitle='', scale='Log', locations=[], maxVal=None,
        isRelative=False, frame=0):

    # TODO: just for tests
    if geolevel == 'dummy':
        geolevel = 'ccaa'

    scales = dict(
        Linear=LinearScale,
        Log=LogScale,
    )
    scaleHigher = maxVal or maxValue(data, geolevel, frame)
    scale = scales[scale](higher=scaleHigher or 1).nice()
    gradient = Gradient('#e0ecbb', '#384413')
    dataDict = dataToTemplateDict(
        data=data,
        colors=gradient,
        title=title,
        subtitle=subtitle,
        locations=locations,
        geolevel=geolevel,
        isRelative=isRelative,
        frame=frame,
        scale=scale
    )
    legend = fillLegend(legendTemplate, scale, gradient, isRelative)
    return template.format(**dataDict, legend=legend)


def toPopulationRelative(data, geolevel, population, perValue=10000):

      # TODO: just for tests
    if geolevel == 'dummy':
        geolevel = 'ccaa'

    populationDict = dict()
    for location in population:
        populationDict.update({location.code: int(location.population)})

    for index in range(len(data.dates)):
        for code, region in iterateLevel(data, geolevel):
            if code == 'None':
                continue
            region["values"][index] = region["values"][index]*perValue / populationDict[code]


def createGif(frameQuantity, data, template, legendTemplate, geolevel, title,
            subtitle='', scale='Log', locations=[],
            isRelative=False, frame=0):

    from wand.image import Image

    maxVal = maxValue(data=data, geolevel=geolevel, frame=frameQuantity - 1)
    with Image() as gif:
        for frame in range(frameQuantity):
            svg = fillMap(
                data=data,
                template=template,
                legendTemplate=legendTemplate,
                title=title,
                subtitle=subtitle,
                locations=locations,
                geolevel=geolevel,
                isRelative=isRelative,
                frame=frame,
                maxVal=maxVal
            )
            with Image(blob=svg.encode('utf8'), format='svg', width=500, height=400) as frame:
                gif.sequence.append(frame)
                with gif.sequence[-1] as frame:
                    frame.delay = 50 # centiseconds
        gif.type = 'optimize'
        gif.format = 'gif'
        return gif.make_blob()


def getNiceDivisor(population):
    from .scale import niceFloorValue
    currentMin = None
    for location in population:
        value = int(location.population)
        if not currentMin or value < currentMin:
            currentMin = value

    return niceFloorValue(currentMin)


def renderMap(source, metric, date, geolevel, isRelative=None, maxValue=None, template=None):
    filtered_objects = source.get(metric, date, [])
    data = aggregate(filtered_objects, geolevel, date)

    locationContent = Path('maps/population_{}.tsv'.format(geolevel)).read_text(encoding='utf8')
    populationPerLocation = tuples2objects(parse_tsv(locationContent))

    locations = [
        location.code for location in populationPerLocation
    ]

    subtitle = ''

    if isRelative:
        perValue = getNiceDivisor(populationPerLocation)
        toPopulationRelative(data, geolevel, populationPerLocation, perValue)
        subtitle = _("per %(num)s population",num="{:,}".format(perValue).replace(',','.'))

    if not template:
        template = Path('maps/mapTemplate_{}.svg'.format(geolevel)).read_text(encoding='utf8')
    
    legendTemplate = Path('maps/legend.svg').read_text(encoding='utf8')

    if len(date) > 1:
        return createGif(
            frameQuantity=len(date),
            data=data,
            template=template,
            legendTemplate=legendTemplate,
            title=metric.title(),
            subtitle=subtitle,
            locations=locations,
            geolevel=geolevel,
            isRelative=isRelative,
        )

    return fillMap(
        data=data,
        template=template,
        legendTemplate=legendTemplate,
        title=metric.title(),
        subtitle=subtitle,
        locations=locations,
        geolevel=geolevel,
        isRelative=isRelative,
    )

# map{Country}{ES}by{States}.svg
# map{Province}{01}by{Counties}.svg

# map.templateName(scope, code, subscope)
# map.subdivisions(scope, code, subscope)
