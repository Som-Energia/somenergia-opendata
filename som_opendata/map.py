from yamlns import namespace as ns
from .mapscale import LinearScale
from .colorscale import Gradient


def dataToTemplateDict(titol, subtitol, data):
    date = data.dates[0]
    result = ns(
            titol = titol,
            subtitol = subtitol,
            year = date.year,
            month = date.month,
        )

    scale = LinearScale(higher=data["values"][0])
    color = Gradient('#e0ecbb','#384413')
    totalValue = data["values"][0]
    for code, ccaa in data.countries.ES.ccaas.items():
        value = ccaa["values"][0]
        result.update({
            'number_' + code: value,
            'percent_' + code: '{:.1f}%'.format(scale(value)*100).replace('.',','),
            'color_' + code: color(scale(value)),
            })
    return result
