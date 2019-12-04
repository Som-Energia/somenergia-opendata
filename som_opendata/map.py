from yamlns import namespace as ns
from .scale import LinearScale, LogScale
from .colorscale import Gradient

months = (
        "Enero Febrero Marzo Abril Mayo Junio "
        "Julio Agosto Septiembre Octubre Noviembre Diciembre"
        ).split()

def percentRegion(value, total):
    return '{:.1f}%'.format(value * 100. / total).replace('.',',')


def dataToTemplateDict(data, colors, titol, subtitol, colorScale='Log', locations=[]):
    date = data.dates[0]
    result = ns(
            titol = titol,
            subtitol = subtitol,
            year = date.year,
            month = months[date.month-1],
        )

    scales = dict(
        Linear = LinearScale,
        Log = LogScale,
    )
    totalValue = data["values"][0]
    scale = scales[colorScale](higher=totalValue)

    for code, ccaa in data.countries.ES.ccaas.items():
        value = ccaa["values"][0]
        result.update({
            'number_' + code: value,
            'percent_' + code: percentRegion(value, totalValue),
            'color_' + code: colors(scale(value)),
            })
    restWorld = data["values"][0] - data.countries.ES["values"][0]
    result.update({
        'number_00': restWorld,
        'percent_00': percentRegion(restWorld,totalValue),
        })

    for code in locations:
        if not result.get('number_{}'.format(code)):
            result.update({
            'number_' + code: 0,
            'percent_' + code: percentRegion(0, totalValue),
            'color_' + code: colors(scale(0)),
                })
    return result


def addEmpty(missing, data):
    missing = str(missing).strip("'").split('_')
    isCCAA = missing[0] in 'number_percent_color_'
    if  not isCCAA:
        raise KeyError(missing)

    ccaa = missing[1]
    data.update({
        'number_' + ccaa: 0,
        'percent_' + ccaa: '0,0%',
        'color_' + ccaa: '#ffffff'})


def fillMap(data, template, gradient, title, subtitle='', scale='Log', locations=[]):

    dataDict = dataToTemplateDict(data=data, colors=gradient, colorScale=scale, titol=title, subtitol=subtitle)

    return template.format(**dataDict)

