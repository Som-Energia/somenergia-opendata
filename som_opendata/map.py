from yamlns import namespace as ns


def dataToSvgDict(titol, subtitol, data):
    date = data.dates[0]
    return ns(
            titol = titol,
            subtitol = subtitol,
            year = date.year,
            month = date.month,
        )
