from yamlns import namespace as ns


def dataToSvgDict(titol, subtitol, data):
    date = data.dates[0]
    result = ns(
            titol = titol,
            subtitol = subtitol,
            year = date.year,
            month = date.month,
        )
    if not data.countries.ES.ccaas:
        return result

    totalValue = data["values"][0]
    for code, ccaa in data.countries.ES.ccaas.items():
        value = ccaa["values"][0]
        result.update({
            'number_' + code: value,
            'percent_' + code: '{:.1f}%'.format(value*100./totalValue).replace('.',','),
            'color_' + code: "#fff",
            })
    return result
