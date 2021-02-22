from __future__ import division
from yamlns import namespace as ns
from .scale import LinearScale, LogScale
from .colorscale import Gradient
from .distribution import getAggregated
from pathlib2 import Path
from wand.image import Image
from functools import lru_cache
from . import common
from flask_babel import lazy_gettext as _

def monthName(date):
    months = [
        _("January"),
        _("February"),
        _("March"),
        _("April"),
        _("May"),
        _("June"),
        _("July"),
        _("August"),
        _("September"),
        _("October"),
        _("November"),
        _("December"),
    ]
    return months[date.month-1]

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

      # TODO: just for tests
    if geolevel == 'dummy':
        geolevel = 'ccaa'

    currentMax = 0
    for code, region in iterateLevel(data, geolevel):
        value = region["values"][frame]
        if value > currentMax:
            currentMax = value

    return currentMax


def fillLegend(legendTemplate, scale, colors, isRelative):
    result = dict()
    for num in [0, 25, 50, 75, 100]:
        value = int(scale.inverse(num / 100.))
        if not isRelative:
            #TODO: remove - 0.001 when breaking up with python2
            value = int(round((value - 0.001), -1))
        if isRelative and (num == 25 or num == 75):
            value = ''
        result.update({
            'legendNumber_{}'.format(num): value,
            'legendColor_{}'.format(num): colors(num / 100.)
        })
    return legendTemplate.format(**result)


def dataToTemplateDict(data, colors, scale, title, subtitle,
        locations=[], geolevel='ccaa', frame=0, isRelative=False):
    date = data.dates[frame]
    result = ns(
            title = title,
            subtitle = subtitle,
            year = date.year,
            month = format(monthName(date)),
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
        subtitle='', locations=[], maxVal=None,
        isRelative=False, scale='Log', frameQuantity=1):

    # TODO: just for tests
    if geolevel == 'dummy':
        geolevel = 'ccaa'

    scales = dict(
        Linear=LinearScale,
        Log=LogScale,
    )
    scaleHigher = maxVal or maxValue(data, geolevel, frame=frameQuantity - 1)
    scale = scales[scale](higher=scaleHigher or 1).nice()
    gradient = Gradient('#e0ecbb', '#384413')
    legend = fillLegend(legendTemplate, scale, gradient, isRelative)

    if frameQuantity > 1:
        return createAnimatedSvg(frameQuantity=frameQuantity,
            data=data,
            template=template,
            geolevel=geolevel,
            title=title,
            subtitle=subtitle,
            colors=gradient,
            scale=scale,
            locations=locations,
            legend=legend,
            isRelative=isRelative,
        )
    else:
        dataDict = dataToTemplateDict(
            data=data,
            colors=gradient,
            title=title,
            subtitle=subtitle,
            locations=locations,
            geolevel=geolevel,
            isRelative=isRelative,
            frame=0,
            scale=scale
        )
        return template.format(**dict(dataDict, legend=legend))



def toPopulationRelative(data, geolevel, values=ns(), perValue=10000):

      # TODO: just for tests
    if geolevel == 'dummy':
        geolevel = 'ccaa'

    populationDict = values
    for index in range(len(data.dates)):
        for code, region in iterateLevel(data, geolevel):
            if code == 'None':
                continue
            region["values"][index] = region["values"][index]*float(perValue) / populationDict[code]

def getNiceDivisor(population):
    from .scale import niceFloorValue
    currentMin = None
    for code, value in population.items():
        if not currentMin or value < currentMin:
            currentMin = value

    return niceFloorValue(currentMin)

def renderMap(source, metric, geolevel, template, locationsCodes, timeDomain=None, relativeMetricValues={}, legendTemplate=''):
    data = getAggregated(
        source=source,
        metric=metric,
        timeDomain=timeDomain,
        location_filter={},
        geolevel=geolevel,
        mutable=bool(relativeMetricValues),
    )
    subtitle = ''

    if relativeMetricValues:
        perValue = getNiceDivisor(relativeMetricValues)
        toPopulationRelative(data=data, geolevel=geolevel, perValue=perValue, values=relativeMetricValues)
        subtitle = _("per %(num)s population", num="{:,}".format(perValue).replace(',','.'))

    title = format(common.metrics[metric].text).title()

    return fillMap(
        data=data,
        template=template,
        legendTemplate=legendTemplate,
        title=title,
        subtitle=subtitle,
        locations=locationsCodes,
        geolevel=geolevel,
        isRelative=bool(relativeMetricValues),
        frameQuantity=len(timeDomain.requestDates),
    )

def frameCssAnimation(frames, seconds, classtemplate):
    """Returns a css with classes to do a frame by frame animation.
    Elements with the given class will be visible just for a frame.
    """
    return ''.join([
        "@keyframes {name} {{ "
            "0% {{ visibility: hidden; }} "
            "{start:.02f}% {{ visibility: visible; }} "
            "{end:.02f}% {{ visibility: hidden; }} "
            "}} "
        ".{name} {{ animation: {name} {seconds}s step-end infinite; }}"
        "\n"
        .format(
            name = classtemplate.format(i),
            start = i * 100. / frames,
            end = (i+1) * 100. / frames,
            seconds = seconds,
            )
        for i in range(frames)
        ])

def createAnimatedSvg(frameQuantity, data, template, legend, geolevel, title, colors, scale, subtitle='', locations=[], isRelative=False):
    templateLines = template.splitlines()
    header, template, tail = templateLines[0], ''.join(templateLines[1:-1]), templateLines[-1]
    frameSeconds = 1.2
    durationSeconds = frameQuantity*frameSeconds

    svgFrames = []
    for frame in range(frameQuantity):
        dataDict = dataToTemplateDict(
            data=data,
            colors=colors,
            title=title,
            subtitle=subtitle,
            locations=locations,
            geolevel=geolevel,
            isRelative=isRelative,
            frame=frame,
            scale=scale
        )
        svg = template.format(**dict(dataDict, legend=legend))
        svgFrames.append(svg)
    return '\n'.join([
        header,
        '<style>',
        frameCssAnimation(
            frames=frameQuantity,
            seconds=durationSeconds,
            classtemplate="frame{:03d}",
        ),
        '</style>',
    ] + [
        '<g class="frame{:03d}">\n{}</g>'.format(i,frame)
        for i,frame in enumerate(svgFrames)
    ] + [
        tail,
    ]).encode('utf8')


# map{Country}{ES}by{States}.svg
# map{Province}{01}by{Counties}.svg

# map.templateName(scope, code, subscope)
# map.subdivisions(scope, code, subscope)
