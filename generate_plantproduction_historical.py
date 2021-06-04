#!/usr/bin/env python3

# Ongoing experiment: taking historical plant production from GDrive
# document from Projects Team.

from sheetfetcher import SheetFetcher
from consolemsg import step, warn
from pathlib import Path

months = (
    "Gener Febrer Març Abril "
    "Maig Juny Juliol Agost "
    "Setembre Octubre Novembre Desembre"
).split()

inecodes = {
    name : code
    for code, name in [
        ('25120','Lleida'),
        ('17148','Riudarenes'),
        ('25228','Torrefarrera'),
        ('08112','Manlleu'),
        ('46193','Picanya'),
        ('25230','Torregrossa'),
        ('47114','Peñafiel'),
        ('41006','Alcolea del Rio'), # tilde mising in drive
        ('41055','Lora del Rio'), # tilde mising in drive
        ('05074','Fontiveros'),
        ('05074','Fontivsolar'), # wrong city name
        ('04090','Tahal'),
        ('18152','Pedro Martínez'),
    ]
}

def sheetFromDrive(certificate, document, sheet):
    step('Baixant produccio...')
    fetcher = SheetFetcher(
        documentName=document,
        credentialFilename=certificate,
        )
    info = fetcher.get_fullsheet(sheet)
    info = [[x.strip() for x in row] for row in info]
    return info

def fromCsv(filename):
    return [
        [x.strip() for x in row.split("\t")]
        for row in Path(filename).read_text(encoding='utf8').split('\n')
    ]

def toCsv(filename, data):
    Path(filename).write_text(
        "\n".join(
            "\t".join(
                str(cell) for cell in row
            )
            for row in data
        )
    )

def toIso(year, month):
    # According opendata conventions energy produced during January
    # (from 2011-01-01 to 2011-01-31) should be tagged 2011-02-01
    if month==months[-1]:
        return f"{int(year)+1}-01-01"
    return f"{int(year)}-{months.index(month)+2:02d}-01"

result = {}
def processPlant(plant, city):
    step(f"Plant {plant} - {city}")
    result[plant] = dict(
        name = plant,
        city = city,
        city_code = inecodes[city],
        vals = {}
    )

def processDataItem(plant, year, month, value):
    value = value.replace('.','')
    value = value or '0'
    value = int(value)
    step(f"Data {plant} {toIso(year,month)} {year} {month} {value}")
    result[plant][toIso(year, month)] = value


def parseblock(info):
    plants = [
        (i, plant, city)
        for i, (plant, city) in enumerate(zip(info[0],info[1]))
        if plant.strip()
    ]
    print(plants)
    for column, plant, city in plants:
        if plant == 'MWh': break # HACK for the additional info at the end
        processPlant(plant, city)
        step(f"plant {plant}")
        year = None
        for irow, row in enumerate(info[2:],2):
            key, val = row[column:column+2]
            if not key and not val: continue
            if year is None and key.isnumeric() :
                year = key
                step(f"year {year}")
                continue
            if key in months:
                month = key
                production_kwh = val
                processDataItem(plant, year, month, production_kwh)
                if month == months[-1]:
                    year = None
                continue
            if key:
                warn(f"repeat at row {irow}")
                break

            warn("Ignored '{}' -> '{}'",
                row[column], row[column+1]
            )

def headerBlocks(rows):
    """
    Since a second set of plants are on rows below the first set,
    this function detects the rows for the plant headers, and splits
    a block for each set.
    """
    step("Detecting plant headers")
    headerRows=[]
    for irow, row in enumerate(rows):
        if not row[0]: continue # empty row
        if row[0] in months: continue # month name
        if row[0].isnumeric(): continue # year
        if irow-1 in headerRows: continue # city row, next to plant header row
        headerRows.append(irow) # That's it!
    # once we have the header row indexes, slice rows in blocks
    return [
        rows[i:j]
        for i,j in zip(
            headerRows,
            headerRows[1:]+[None]
        )
    ]

def dump(result, csvfile):
    """
    Dumps final data.
    """
    alldates = set()
    for plant in result.values():
        alldates.update(plant.keys())

    for plant in result.values():
        for date in alldates:
            plant.setdefault(date,0)

    headers = ['name', 'city_code', 'city'] + list(sorted(alldates))
    output = [ headers ]
    for plant in result.values():
        output.append(
            [plant[header] for header in headers]
        )
    toCsv(csvfile, output)

keep=False
originalDataFile = Path("historical-production-sheet.csv")
if keep:
    # Avoid download to develop parsing faster
    info = fromCsv(originalDataFile)
else:
    info = sheetFromDrive(
        certificate = 'drive-certificate.json',
        document = 'Control de instalaciones_Gestió d\'Actius',
        sheet = 'Històric producció',
    )
    toCsv(originalDataFile, info)

blocks = headerBlocks(info)
for block in blocks:
    parseblock(block)

dump(result, "plantproduction-historical.csv")


