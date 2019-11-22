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

    code = '01'
    ccaa = data.countries.ES.ccaas[code]
    result.update({
        'number_' + code: ccaa["values"][0],
        'percent_' + code: 100,
        'color_' + code: "#fff",
        })
    return result
