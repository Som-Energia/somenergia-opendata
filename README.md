# somenergia-opendata

[![Build Status](https://travis-ci.org/Som-Energia/somenergia-opendata.svg?branch=master)](https://travis-ci.org/Som-Energia/somenergia-opendata)

Public API to access open data information about the cooperative

- API UI: https://opendata.somenergia.coop/ui/
- API Documentation: https://opendata.somenergia.coop/docs/

## Example queries


### Geographical distributions


- `/contracts`
    All current contracts

- `/members`
    All current members (instead of contracts)

- `/contracts/on/2018-02-03`
    Contracts on a given date

- `/contracts/by/city`
    Current contracts aggregated by city

- `/contracts/by/city/on/2018-02-03`
    Contracts aggregated by city at a given date

- `/contracts/by/city/weekly`
    Contracts aggregated by city every available week

- `/contracts/by/state/monthly`
    Contracts aggregated by state every available month

- `/contracts/by/ccaa/yearly`
    Contracts aggregated by CCAA every available year

- `/contracts/by/city/weekly/from/2018-02-03`
    Contracts aggregated by state every week from a date

- `/contracts/by/city/weekly/from/2018-02-03/to/2018-05-05`
    Contracts aggregated by city every week from a date until a date

- `/contracts/by/city/weekly/to/2018-05-05`
    Contracts aggregated by city every week until a date


#### Using filters


- `/contracts/by/city?city=23423&city=89545`
    Include just cities with INE code 23423 and 89545

- `/contracts/by/city?city=23423&city=89545&ccaa=04`
    Include just cities with INE code 23423 and 89545 and also all cities from CCAA 04 (Catalonia)

- `/contracts/by/city?state=004`
    Include just cities in state 004

#### Response format

TODO

### Maps

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
    Gif animation with contracts by state every available month

- `/map/contracts/by/ccaa/yearly`
    Gif animation with contracts aggregated by CCAA every available year

- `/map/contracts/by/state/monthly/from/2018-02-01`
    Gif animation with contracts aggregated by state every month from a date

- `/map/contracts/by/state/monthly/from/2018-02-03/to/2018-05-01`
    Gif animation with contracts aggregated by state every month from a date until a date

- `/map/contracts/by/state/monthly/to/2018-05-01`
    Gif animation with contracts aggregated by state every month until a date

### External sources


- https://analisi.transparenciacatalunya.cat/Sector-P-blic/Caps-de-municipi-de-Catalunya-georeferenciats/wpyq-we8x
	- wget https://analisi.transparenciacatalunya.cat/resource/wpyq-we8x.csv -O Caps_de_municipi_de_Catalunya_georeferenciats.csv


## Requirements

```bash
sudo apt install libmagickwand-dev inkscape
```

## Translations

### Languages supported

- Catalan (ca)
- Spanish (es)
- Euskara (eu)
- Galician (gl)

### To Compile Language Translations

- `pybabel compile -f -d som_opendata/translations` 
