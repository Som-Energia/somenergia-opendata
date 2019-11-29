from yamlns import namespace as ns
from .mapscale import LinearScale, LogScale
from .colorscale import Gradient

months = (
        "Enero Febrero Marzo Abril Mayo Junio "
        "Julio Agosto Septiembre Octubre Noviembre Diciembre"
        ).split()

def dataToTemplateDict(titol, subtitol, data, colors, colorScale='Linear'):
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
    color = Gradient('#e0ecbb','#384413')
    totalValue = data["values"][0]
    for code, ccaa in data.countries.ES.ccaas.items():
        value = ccaa["values"][0]
        result.update({
            'number_' + code: value,
            'percent_' + code: '{:.1f}%'.format(value * 100. / totalValue).replace('.',','),
            'color_' + code: colors(scale(value)),
            })
    restWorld = data["values"][0] - data.countries.ES["values"][0]
    result.update({
        'number_00': restWorld,
        'percent_00': '{:.1f}%'.format(restWorld * 100. / totalValue).replace('.',','),
        })
    return result


def renderMap(data, template):
    with open(template,'r') as svgTemplateFile:
        svgTemplate = svgTemplateFile.read()

    svgContent = svgTemplate.format(**data)

    return svgContent
