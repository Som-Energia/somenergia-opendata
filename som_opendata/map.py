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

    if colorScale == 'Linear':
        scale = LinearScale(higher=data["values"][0])
    elif colorScale == 'Log':
        scale = LogScale(higher=data["values"][0])

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
    data.update({missing: 0})
    # if 'number_' in missing:
    #     ccaa = missing.split('_')[1]
    #     data.update({
    #         'number_' + ccaa : 0,
    #         'percent_' + ccaa: '0,0%',
    #         'color_' + ccaa: '#fff',
    #         })
    # else:
    #     return False, 
    # return success,data

def renderMap(data, template, colors, title, subtitle='', colorScale='Log'):

    dataDict = dataToTemplateDict(data=data, colors=colors, colorScale=colorScale, titol=title, subtitol=subtitle)

    with open(template, 'r') as svgTemplateFile:
        svgTemplate = svgTemplateFile.read()

    finished = False
    while not finished:
        try:
            svgContent = svgTemplate.format(**dataDict)
            finished = True
        except KeyError as ke:
            addEmpty(missing=ke, data=dataDict)
            finished = True
    return svgContent
