from __future__ import division
from yamlns import namespace as ns
from .scale import LinearScale, LogScale
from .colorscale import Gradient
from .distribution import aggregate, parse_tsv, tuples2objects
from pathlib2 import Path


months = (
        "Enero Febrero Marzo Abril Mayo Junio "
        "Julio Agosto Septiembre Octubre Noviembre Diciembre"
        ).split()


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


def fillLegend(result, scale, colors, isRelative):
    for num in [0, 25, 50, 75, 100]:
        value = int(scale.inverse(num / 100))
        if not isRelative:
            value = round(value, -1)
        if isRelative and (num == 25 or num == 75):
            value = ''
        result.update({
            'legendNumber_{}'.format(num): value,
            'legendColor_{}'.format(num): colors(num / 100)
        })


def dataToTemplateDict(data, colors, title, subtitle,
        colorScale='Log', locations=[], geolevel='ccaa',
        maxVal=None, frame=0, isRelative=False):
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
    fillLegend(result, scale, colors, isRelative)

    return result


def fillMap(data, template, geolevel, title,
        subtitle='', scale='Log', locations=[], maxVal=None,
        isRelative=False, frame=0):
    gradient = Gradient('#e0ecbb', '#384413')

    dataDict = dataToTemplateDict(
        data=data,
        colors=gradient,
        colorScale=scale,
        title=title,
        subtitle=subtitle,
        locations=locations,
        geolevel=geolevel,
        maxVal=maxVal,
        isRelative=isRelative,
        frame=frame
    )
    return template.format(**dataDict)


def toPopulationRelative(data, geolevel, population):

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
            region["values"][index] = region["values"][index]*10000 / populationDict[code]


def createGif(filename, frameQuantity, data, template, geolevel, title,
            subtitle='', scale='Log', locations=[],
            isRelative=False, frame=0):

    from wand.image import Image

    maxVal = maxValue(data=data, geolevel=geolevel, frame=frameQuantity - 1)
    with Image() as gif:
        for frame in range(frameQuantity):
            try:
                svg = fillMap(
                    data=data,
                    template=template,
                    title=title,
                    subtitle=subtitle,
                    locations=locations,
                    geolevel=geolevel,
                    isRelative=isRelative,
                    frame=frame,
                    maxVal=maxVal
                )
            except:
                continue
            with Image(blob=svg.encode('utf8'), format='svg', width=500, height=400) as frame:
                gif.sequence.append(frame)
                with gif.sequence[-1] as frame:
                    frame.delay = 50 # centiseconds
        gif.type = 'optimize'
        gif.save(filename=filename)

def renderMap(source, metric, date, geolevel, isRelative=None, maxValue=None):
    locationContent = Path('maps/population_{}.tsv'.format(geolevel)).read_text(encoding='utf8')
    populationPerLocation = tuples2objects(parse_tsv(locationContent))

    locations = [
        location.code for location in populationPerLocation
    ]

    filtered_objects = source.get(metric, date, [])
    data = aggregate(filtered_objects, geolevel)
    subtitle = ''

    if isRelative:
        toPopulationRelative(data, geolevel, populationPerLocation)
        subtitle = "/10.000 hab"
    template = Path('maps/mapTemplate_{}.svg'.format(geolevel)).read_text(encoding='utf8')

    if len(date) > 1:
        filename="map-{}-{}-{}-{}.gif".format(metric, geolevel, date[0], date[-1])
        createGif(filename=filename,
            frameQuantity=len(date),
            data=data,
            template=template,
            title=metric.title(),
            subtitle=subtitle,
            locations=locations,
            geolevel=geolevel,
            isRelative=isRelative,
        )
        return Path('{}.gif'.format(filename)))

    return fillMap(
        data=data,
        template=template,
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
