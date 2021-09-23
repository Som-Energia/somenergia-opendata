# somenergia-opendata

[![Build Status](https://app.travis-ci.com/Som-Energia/somenergia-opendata.svg?branch=master)](https://app.travis-ci.com/Som-Energia/somenergia-opendata)
[![Coverage Status](https://coveralls.io/repos/github/Som-Energia/somenergia-opendata/badge.svg?branch=master)](https://coveralls.io/github/Som-Energia/somenergia-opendata?branch=master)


Public API to access open data information about the cooperative

- API UI: https://opendata.somenergia.coop/ui/
- API Documentation: https://opendata.somenergia.coop/docs/
- API Base: https://opendata.somenergia.coop/v0.2/

## Example queries


### Numerical data

Follow the following structure `/<metric>[/by/<geolevel>][/on/<date>|[/monthly|/yearly][/from/<date>][/to/<date>]]`

- `/contracts`
    All current contracts

- `/members`
    All current members (instead of contracts)

- `/newcontracts`
    New contracts last month (same for members)

- `/canceledcontracts`
    Leaving contracts last month (same will do for members)

- `/contracts/on/2018-02-01`
    Contracts on a given date (just firsts of month allowed)

- `/contracts/by/city`
    Current contracts aggregated by city

- `/contracts/by/city/on/2018-02-01`
    Contracts aggregated by city at a given date

- `/contracts/by/state/monthly`
    Contracts aggregated by state every available month

- `/contracts/by/ccaa/yearly`
    Contracts aggregated by CCAA every available year

- `/contracts/by/city/monthly/from/2018-02-01`
    Contracts aggregated by state every week from a date

- `/contracts/by/city/yearly/from/2018-02-01/to/2018-05-01`
    Contracts aggregated by city every week from a date until a date

- `/contracts/by/city/weekly/to/2018-05-01`
    Contracts aggregated by city every week until a date

### Using filters

You can append repeatedly query params to filter data just including some geografical regions:

- `/contracts/by/city?city=23423&city=89545`
    Include just cities with INE code 23423 and 89545

- `/contracts/by/city?city=23423&city=89545&ccaa=04`
    Include just cities with INE code 23423 and 89545 and also all cities from CCAA 04 (Catalonia)

- `/contracts/by/city?state=04`
    Include just cities in state 04

#### Response format

Data is returned in YAML.
It has a hierarchical structure from the world geographical level to the requested geographical level of detail (country in this example)
Each region has as many numbers in list as the top level `dates`.

```yaml
dates:
- 2014-01-01
- 2015-01-01
- 2016-01-01
values:
- 11905
- 17896
- 23749
countries:
  CL:
    name: Chile
    values:
    - 1
    - 1
    - 1
  ES:
    name: España
    values:
    - 11896
    - 17885
    - 23738
  FR:
    name: France
    values:
    - 1
    - 1
    - 1
  DE:
    name: Germany
    values:
    - 1
    - 2
    - 2
  GR:
    name: Greece
    values:
    - 0
    - 0
    - 0
  NL:
    name: Netherlands
    values:
    - 3
    - 3
    - 3
  PT:
    name: Portugal
    values:
    - 1
    - 1
    - 1
  UK:
    name: United Kingdom
    values:
    - 2
    - 2
    - 2
  None:
    name: None
    values:
    - 0
    - 1
    - 1
```

### Maps

All maps are returned as SVG files.
Follow the following structure `/map/<metric>[/per/<relative>][/by/<geolevel>][/on/<date>|[/monthly|/yearly][/from/<date>][/to/<date>]]`

- `/map/contracts`
    All current contracts by ccaa

- `/map/contracts?lang=es`
    All current contracts by ccaa in Spanish

- `/map/members`
    All current members by ccaa

- `/map/contracts/on/2018-02-03`
    Contracts on a given date

- `/map/contracts/by/state`
    Current contracts aggregated by state

- `/map/contracts/per/population/by/state`
    Current contracts relatives to population aggregated by state

- `/map/contracts/by/state/on/2018-02-03`
    Contracts aggregated by state at a given date

- `/map/contracts/by/state/monthly`
    Animation with contracts by state every available month

- `/map/contracts/by/ccaa/yearly`
    Animation with contracts aggregated by CCAA every available year

- `/map/contracts/by/state/monthly/from/2018-02-01`
    Animation with contracts aggregated by state every month from a date

- `/map/contracts/by/state/monthly/from/2018-02-03/to/2018-05-01`
    Animation with contracts aggregated by state every month from a date until a date

- `/map/contracts/by/state/monthly/to/2018-05-01`
    Animation with contracts aggregated by state every month until a date

- `/map/contracts/by/city/monthly/to/2018-05-01?localgroup=BaixMontseny`
    Animation with contracts aggregated by city within localgroup BaixMontseny every month until a date


### Discovery

- `/discover/metrics`
    Shows all suported metrics as a list named `metrics` with
    - `id` the id used to refer the metric
    - `text` the translated text to display users
    - `description` translated text with detailed explanation of the meaning, source and errors of the metric

- `/discover/geolevel`
    Returns a list `geolevels` with the supported geolevels and related info
    - `id` is the id used to refer it (its a mnemonic id)
    - `text` is the translated text to display users
    - `plural` is the pluralization of id used in yaml's as key when many are given
    - `parent` tells which other geolevel fully contains its subdivisions.
    - `detailable: false` tells that a geolevel is not supported as statistics detail level (optional, default `true`)
    - `mapable: false` tells that a geolevel is not supported as map detail level (optional, default `true`)

- `/discover/geolevel/ccaa`
    Returns a list of divisions at the `ccaa` level as a map `options` with id -> text

- `/discover/geolevel/city?localgroup=BaixLlobregat`
    Limits the list of cities to the ones included in the localgroup `BaixLlobregat`

- `/discover/geolevel/localgroup?ccaa=09`
    Lists all the localgroups working on areas covering cities in Catalonia (09)



### Language

Whenever human readable strings are returned,
browser language is used by default (accept-language http header).
Language can be forced by using `lang` query parameter.

If the language is not specified in either form or the one selected is not supported, spanish is chosen.
But that could be changed in the future to english.
So, if you want spanish, please, specify it.

Supported languages are:

- Catalan (ca)
- Spanish (es)
- Euskara (eu)
- Galician (gl)

## Deploy

### Requirements

```bash
sudo apt install libmagickwand-dev inkscape libyaml-dev
python setup.py develop
```

### Compile Language Translations

WARNING: Some back-to-back tests will fail if language files are not generated.

```bash
./setup.py compile_catalog
```

Default options are specified in setup.cfg

In order to incorporate new strings from code:

```bash
./setup.py extract_messages # generates a new pot file with all extracted strings
./setup.py update_catalog # Merges all translations with new strings
```

More info about translation management on http://babel.pocoo.org/en/latest/setup.html

### Generate documentation

```bash
npm install
npm run redocs
```

### Testing

Tests are unittest based, using either nosetests or pytest as runner is recommended.

```bash
TRAVIS=1 pytest som_opendata
```

`TRAVIS=1` will disable tests for code directly using SomEnergia databases.
Mainly queries to extract annonymized by aggregation from non-annonymized original data.

Notice: Some tests require translation catalog to be generated. See above.

### Profiling and optimizing

In order to optimize the api, first profile the entry point to detect
the bottle necks, you that your efforts are better targeted
and to have an objective measure of your progress.

```bash
sudo apt install pyprof2calltree kcachegrind
pip install pytest-profiling
PROFILE=1 pytest --profile -v som_opendata/api_test.py::Api_Test::test__profiling
pyprof2calltree -i prof/combined.prof -o profiling-$(date -Iseconds).out
```

### Releasing

- Generate language strings (see above)
- Update version in:
  - `som_opendata/__init__.py`
  - `package.json`
  - `openapi.yaml`
  - `som_opendata/api.py`
- Generate the documentation (see above)
- Update the CHANGES.md (replace `unreleased` by the actual release date)
- Commit the version bump
- tag it opendata-M.m.r


## External data sources

### Could be used in the future

- For counties (comarques) and city population in Catalonia
  - https://analisi.transparenciacatalunya.cat/Sector-P-blic/Caps-de-municipi-de-Catalunya-georeferenciats/wpyq-we8x
    - wget https://analisi.transparenciacatalunya.cat/resource/wpyq-we8x.csv -O Caps_de_municipi_de_Catalunya_georeferenciats.csv




