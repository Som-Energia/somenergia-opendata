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

    for code, ccaa in data.countries.ES.ccaas.items():
        result.update({
            'number_' + code: ccaa["values"][0],
            'percent_' + code: 100,
            'color_' + code: "#fff",
            })
    return result
