from yamlns import namespace as ns


def dataToSvgDict(titol, subtitol):
    
    return ns.loads("""\
            titol: un títol
            subtitol: un subtítol
            year: 2019
            month: 1
        """)
