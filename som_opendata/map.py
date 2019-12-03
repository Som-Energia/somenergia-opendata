from yamlns import namespace as ns
from .mapscale import LinearScale, LogScale
from .colorscale import Gradient

months = (
        "Enero Febrero Marzo Abril Mayo Junio "
        "Julio Agosto Septiembre Octubre Noviembre Diciembre"
        ).split()

def percentRegion(value, total):
    return '{:.1f}%'.format(value * 100. / total).replace('.',',')


def dataToTemplateDict(data, colors, titol, subtitol, colorScale='Log'):
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
    scale = scales[colorScale](higher=data["values"][0])

    totalValue = data["values"][0]
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
    return result


def addEmpty(missing, data):
    missing = str(missing).strip("'").split('_')
    isCCAA = missing[0] in 'number_percent_color_'
    if isCCAA:
        ccaa = missing[1]
        data.update({
            'number_' + ccaa: 0,
            'percent_' + ccaa: '0,0%',
            'color_' + ccaa: '#ffffff'})
    else:
        raise KeyError(missing)


def fillMap(data, template, gradient, title, subtitle='', scale='Log'):

    dataDict = dataToTemplateDict(data=data, colors=gradient, colorScale=scale, titol=title, subtitol=subtitle)

    return template.format(**dataDict)

