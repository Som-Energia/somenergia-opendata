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

    result.update(
        number_01=123,
        percent_01=100,
        color_01="#fff",
        )
    return result
