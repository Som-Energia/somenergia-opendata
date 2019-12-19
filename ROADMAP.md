# ROADMAP 

## API 1.0

We want to be able to express:

Introspeccio:
- Quines metriques estan suportades
- Quins geolevels estan suportats (ccaa, state...)
- Quins codis y noms hi ha a un determinat geolevel amb possible filtre
- Quins formats disponibles per un tipus de query (mapa, distribution)
- Quins filtres s'apliquen als tags

/discover/metric
/discover/geolevel  [ccaa, city, state, country, county, localgrup...]
/discover/geolevel/country?continent=Europe    {ES:España,...}
/discover/geolevel/city?ccaa=09    {0808: barcelona, :}
/discover/geolevel/localgroup
/discover/geolevel/city?localgroup=BaixMontseny
/discover/format/distribution
/discover/format/map
/discover/aspect/production  {tecnology, }
/discover/metric/


tecnology=biogas
financedby=generationkwh
financedby=aportacions


Metriques relatives (poblacio)

Distributions:
- Format (csv, yaml, json...)
- Distribucions relatives (members/poblacio)
- Diferencial
- Integral
- Filtres per tag associats a la metrica

Maps:
- Format (svg, gif, png, mng...)
- Distribucions relatives
- Diferencial
- Integral
- Filtres per tag associats a la metrica

Esdeveniments
- ???

Widgets
Webapps

/members/by/state/monthly/from/2019-10-01/to/2019-11-01?format=json

/map/members/by/state/monthly/from/2019-10-01/to/2019-11-01?format=png&diff=1

/map/members/per/population/by/state/monthly/from/2019-10-01/to/2019-11-01?format=png&diff=1

/production/by/state/monthly/from/2019-10-01/to/2019-11-01?tag=biogas


## El de hoy hoy


- field -> metric
- metric de tipus string, i afegir el check que retorni error informatiu
- geolevel de tipus string, i afegir el check que retorni error informatiu
- frequency de tipus string, i afegir el check que retorni error informatiu
- dateSequences: takes first day of week, month, year...
- Fragilitat dels testos B2B de csv's amb l'ordre segons l'idioma del sistema
- Actualitzar les dades del csv
- Revisar SQL members


## El de hoy


- TDD de requestedDates(firstDate, onDate, fromDate, toDate, periodicity): dates
- TDD de pickDates(tuples, dates): tuples
- TDD de la api contra cvs' sinteticos que no fallen
- Considerar los casos que falln
- Decidir un punto de la cascada de lo que sera un Source. Eso definira,
	- que parametros necesita
	- cual es el formato de salida
- TDD Unittest CsvSource
- Refactoring substitucion de la cadena `members_modul.source` de texto tsv







## Casos d'ús

Recopilar usos que ens podem imaginar que ens facin de l'api

- Dades per farcir el mapa de municipis de somlabs
- Dades per farcir els mapes que enviem als grups locals
	- Provincies/Comunitats
	- Socis/Contractes
	- Relatius/Absoluts
- Creixement per setmana per comparar-ho amb els events d'un grup local
- Dades per construir gifs animats dels mapes

## Requeriments

- Especificar un interval de dates
- Limitar a un ambit geografic
- Mostrar o no els sumaris dels ambits incloents
- Limitar el detall als ambits geografics inferiors
- Filtrar contractes per potencia o tarifa


## Testos unitaris

- Previ:
  - TDD to convert table column names into atribute friendly names f:str -> str
  - TDD: convert tables (tsv) with headers into lists of ns (0,1,2 columnes, 0,1,2 files)
- Objectiu a llarg, construir el yaml sample.yaml
- Primer cas: una taula amb header i "un sol poble", i una sola data
  - el mateix numero a tots nivells
  - green posant l'string tal cual
  - Refactor 1: Anar-ho passat a un ns real amb literals
  - Refactor 2: Agafar els literals de la taula
- Segon cas: dos dates
	- ens obliga a interpretar les dates dels headers (refactor previ)
	- ens obliga a tractar els 'quants' com a un array i convertir-ho
- Tercer cas: Dos pobles de paissos diferents
	- ens obliga a introduir la iteracio per linia
	- hi ha la part comuna que la construirem fora del bucle
	- Afegirem cegament cada linia com a un pais nou (que arriben dos de ES? per aixo tenim el seguent test)
- Quart cas: Mateix pais, diferent comunitat autonoma
	- ens obliga a identificar si el pais ja hi es i si ho es, agregar per pais, sumant els numeros
- Cinquè cas: Mateixa CCAA, diferent state
	- igual que l'anterior pero amb CCAA's
- Sisè cas: Mateix state, diferent city
	- igual que l'anterior, pero amb state
- Seté cas: Refactor extreure codi repetit (searchOrCreate)

- Tercer cas: Dos pobles, una data (de diferents paisos? o de la mateixa provincia?)
	
- Quart cas: Anar pujant o baixant el punt de diferencia ente els dos pobles
- Plantejem el test: dos pobles dos dates, si passa, l'esborrem



## TODO a llarga

- Amb pony, construir la taula
- Cachejar les taules setmanals/mensuals
- Construir mapes
- Construir gifs
- Mesures relatives: Cups, poblacio, cens

## TODO altres temes

- Produccio d'energia
- Demanda d'energia dels nostres contractes









