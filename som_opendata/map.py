from yamlns import namespace as ns
from .scale import LinearScale, LogScale
from .colorscale import Gradient
from .distribution import aggregate, parse_tsv, tuples2objects
from pathlib import Path
from datetime import date, timedelta


months = (
        "Enero Febrero Marzo Abril Mayo Junio "
        "Julio Agosto Septiembre Octubre Noviembre Diciembre"
        ).split()

def percentRegion(value, total):
    if not total:
        return '0,0%'
    return '{:.1f}%'.format(value * 100. / total).replace('.',',')

def dataToTemplateDict(data, colors, title, subtitle, colorScale='Log', locations=[], geolevel='ccaa'):
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
    totalValue = data["values"][0]

    scale = scales[colorScale](higher=totalValue or 1)

    for code, ccaa in data.countries.ES.ccaas.items():
        if geolevel is 'ccaa':
            value = ccaa["values"][0]
            result.update({
                'number_' + code: value,
                'percent_' + code: percentRegion(value, totalValue),
                'color_' + code: colors(scale(value)),
                })
        elif geolevel is 'states':
            for code, state in ccaa.states.items():
                value = state["values"][0]
                result.update({
                    'color_' + code: colors(scale(value)),
                })

    restWorld = data["values"][0] - data.countries.ES["values"][0]
    result.update({
        'number_00': restWorld,
        'percent_00': percentRegion(restWorld,totalValue),
        })

    for code in locations:
        if result.get('number_{}'.format(code)):
            continue
        result.update({
        'number_' + code: 0,
        'percent_' + code: percentRegion(0, totalValue),
        'color_' + code: colors(scale(0)),
        })
    return result


def fillMap(data, template, title, subtitle='', scale='Log', locations=[]):
    gradient = Gradient('#e0ecbb','#384413')
    dataDict = dataToTemplateDict(
        data=data, colors=gradient,
        colorScale=scale, title=title, subtitle=subtitle, locations=locations
    )

    return template.format(**dataDict)

def lastDateWithData():
    today = date.today()
    endLastMonth = today - timedelta(days=today.day)
    return str(endLastMonth.replace(day=1).isoformat())

def renderMap(source, metric, date, geolevel):
    if not date:
        date = lastDateWithData()
    locationContent = Path('maps/population_{}.tsv'.format(geolevel)).read_text(encoding='utf8')
    locations = [
        location.code for location in tuples2objects(parse_tsv(locationContent))
    ]
    filtered_objects = source.get(metric, [date], [])
    data = aggregate(filtered_objects, geolevel)
    template = Path('maps/mapTemplate_{}.svg'.format(geolevel)).read_text(encoding='utf8')
    return fillMap(data=data, template=template, title=metric.title(), locations=locations)


# map{Country}{ES}by{States}.svg
# map{Province}{01}by{Counties}.svg

# map.templateName(scope, code, subscope)
# map.subdivisions(scope, code, subscope)
