define({ "api": [
  {
    "type": "get",
    "url": "/v0.2/discover/geolevel/:geolevel",
    "title": "Available Geolevel values",
    "version": "0.2.15",
    "name": "Geolevels_values",
    "group": "Discover",
    "description": "<p>Returns the available values for a given geografical division</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "options",
            "description": "<p>{Object) Mapping of level codes to its translated display text</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "All Autonomous Comunities",
          "content": "/v0.2/discover/geolevel/ccaa\nHTTP/1.1 200OK\noptions:\n  '01': Andalucia\n  '02': Aragón\n  '03': Asturias, Principado de\n  '04': Baleares, Islas\n  '05': Canarias\n  '06': Cantabria\n  '07': Castilla y León\n  '08': Castilla - La Mancha\n  '09': Cataluña\n  '10': Comunidad Valenciana\n  '11': Extremadura\n  '12': Galicia\n  '13': Madrid, Comunidad de\n  '14': Murcia, Región de\n  '15': Navarra, Comunidad Foral de\n  '16': País Vasco\n  '17': Rioja, La",
          "type": "yaml"
        },
        {
          "title": "All local grups in Catalonia",
          "content": "/v0.2/discover/geolevel/localgroups?ccaa=09\nHTTP/1.1 200OK\noptions:\n  AltPenedes: Alt Penedès\n  Anoia: Anoia\n  Badalona: Badalona\n  Bages: Bages\n  BaixLlobregat: Baix Llobregat\n  BaixMontseny: Baix Montseny\n  BaixValles: Baix Vallès\n  Barcelona: Barcelona\n  CastellarValles: Castellar del Vallès\n  CerdanyolaValles: Cerdanyola del Vallès\n  Maresme: Maresme\n  Osona: Osona\n  Rubi: Rubí\n  Sabadell: Sabadell\n  SantCugatValles: Sant Cugat del Vallès\n  SelvaMaritima: Selva Marítima\n  Terrassa: Terrassa",
          "type": "yaml"
        }
      ]
    },
    "filename": "som_opendata/api.py",
    "groupTitle": "Discover",
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/discover/geolevel/:geolevel"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Enum",
            "allowedValues": [
              "\"country\"",
              "\"ccaa\"",
              "\"state\"",
              "\"city\"",
              "\"localgroup\""
            ],
            "optional": false,
            "field": "geolevel",
            "description": "<p>Geographical detail level, including aliased geolevel alias, like localgroup.</p>"
          }
        ],
        "Query Parameters": [
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "country",
            "description": "<p>ISO codes of the countries to be included</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "ccaa",
            "description": "<p>INE codes of the CCAAs to be included</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "state",
            "description": "<p>INE codes of the states to be included</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "city",
            "description": "<p>INE codes of cities to be included</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "localgroup",
            "description": "<p>Code of the Local Group to be included. It represents an alias of one or more filters.</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String",
            "allowedValues": [
              "\"en\"",
              "\"es\"",
              "\"ca\"",
              "\"gl\"",
              "\"eu\""
            ],
            "optional": true,
            "field": "lang",
            "defaultValue": "browser",
            "description": "<p>defined or en] Forced response language If no language is forced, the one in the browser (Accepted-Language header) is taken. If the languange is not one of the suppoerted, english is taken by default.</p>"
          }
        ]
      }
    }
  },
  {
    "type": "get",
    "url": "/v0.2/discover/geolevel",
    "title": "Available Geolevels",
    "version": "0.2.15",
    "name": "GetGeolevels_lala",
    "group": "Discover",
    "description": "<p>Returns the geolevels (geographical levels) that can be used in queries, such as countries, states, cities</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "geolevels",
            "description": "<p>List of geolevels</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "geolevels.id",
            "description": "<p>The id to refer the geolevel</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "geolevels.text",
            "description": "<p>Translated text to show users</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": true,
            "field": "geolevels.plural",
            "defaultValue": "id+\"s\"",
            "description": "<p>Plural tag to use in structures</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": true,
            "field": "geolevels.parent",
            "defaultValue": "null",
            "description": "<p>The parent geolevel</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": true,
            "field": "geolevels.detailed",
            "defaultValue": "true",
            "description": "<p>Set to false if it is not supported as level of detail for distributions</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": true,
            "field": "geolevels.mapable",
            "defaultValue": "true",
            "description": "<p>Set to false if it is not supported as level of detail for map</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\ngeolevels:\n- id: world\n  text: 'World'\n  mapable: False\n- id: country\n  text: 'Country'\n  parent: world\n  plural: countries\n  mapable: False\n- id: ccaa\n  text: 'CCAA'\n  parent: country\n  plural: ccaas\n- id: state\n  text: 'State'\n  parent: ccaa \n  plural: states\n- id: city\n  text: 'City'\n  parent: state\n  plural: cities\n  mapable: False\n- id: localgroup\n  text: 'Local Group'\n  parent: world\n  plural: localgroups\n  detailed: False\n  mapable: False",
          "type": "yaml"
        }
      ]
    },
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/discover/geolevel"
      }
    ],
    "filename": "som_opendata/api.py",
    "groupTitle": "Discover",
    "parameter": {
      "fields": {
        "Query Parameters": [
          {
            "group": "Query Parameters",
            "type": "String",
            "allowedValues": [
              "\"en\"",
              "\"es\"",
              "\"ca\"",
              "\"gl\"",
              "\"eu\""
            ],
            "optional": true,
            "field": "lang",
            "defaultValue": "browser",
            "description": "<p>defined or en] Forced response language If no language is forced, the one in the browser (Accepted-Language header) is taken. If the languange is not one of the suppoerted, english is taken by default.</p>"
          }
        ]
      }
    }
  },
  {
    "type": "get",
    "url": "/v0.2/discover/metrics",
    "title": "Available metrics",
    "version": "0.2.15",
    "name": "GetMetrics",
    "group": "Discover",
    "description": "<p>Returns the metrics that can be queried.</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "metrics",
            "description": "<p>List of metrics</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "metrics.id",
            "description": "<p>The id to refer the metric</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "metrics.text",
            "description": "<p>Translated text to show users</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "metrics.description",
            "description": "<p>Translated Markdown text explaining the metric</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\nmetrics:\n- id: members\n  text: 'Members'\n  description: \"Members of the cooperative at the end of the day.\"\n- id: contracts\n  text: 'Contracts'\n  description: \"Active contracts at the end of the day.\"",
          "type": "yaml"
        }
      ]
    },
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/discover/metrics"
      }
    ],
    "filename": "som_opendata/api.py",
    "groupTitle": "Discover",
    "parameter": {
      "fields": {
        "Query Parameters": [
          {
            "group": "Query Parameters",
            "type": "String",
            "allowedValues": [
              "\"en\"",
              "\"es\"",
              "\"ca\"",
              "\"gl\"",
              "\"eu\""
            ],
            "optional": true,
            "field": "lang",
            "defaultValue": "browser",
            "description": "<p>defined or en] Forced response language If no language is forced, the one in the browser (Accepted-Language header) is taken. If the languange is not one of the suppoerted, english is taken by default.</p>"
          }
        ]
      }
    }
  },
  {
    "type": "get",
    "url": "/v0.2/:metric/by/:geolevel/on/:ondate",
    "title": "Metric Data on a Given Date",
    "version": "0.2.15",
    "group": "Distribution",
    "name": "Distribution",
    "description": "<p>Returns the geographical distribution of a metric at a given date.</p> <p>Use the filters in the query string to restrict to a group of geographical entities. The filters are additive. That means that any city matching any of the specified values will be counted.</p>",
    "examples": [
      {
        "title": "Current number of contracts",
        "content": "/v0.2/contracts",
        "type": "json"
      },
      {
        "title": "Current members at every state",
        "content": "/v0.2/members/by/state",
        "type": "json"
      },
      {
        "title": "Members at every CCAA on 2018-02-01",
        "content": "/v0.2/members/by/ccaa/on/2018-02-01",
        "type": "json"
      },
      {
        "title": "Members by city on Araba and Gipuzcoa provinces",
        "content": "/v0.2/members/by/city?state=01&state=20",
        "type": "json"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"contracts\"",
              "\"members\""
            ],
            "optional": false,
            "field": "metric",
            "description": "<p>Quantity to aggregate.</p>"
          },
          {
            "group": "Parameter",
            "type": "Enum",
            "allowedValues": [
              "country",
              "ccaa",
              "state",
              "city"
            ],
            "optional": true,
            "field": "geolevel",
            "defaultValue": "world",
            "description": "<p>Geographical detail level. Use the geolevel to get more geographical detail (country, ccaa, state, city). For just global numbers, remove the whole <code>/by/:geolevel</code> portion of the path.</p>"
          },
          {
            "group": "Parameter",
            "type": "Date",
            "optional": true,
            "field": "ondate",
            "description": "<p>Single date, in ISO format (YYYY-MM-DD). To obtain the last available data, remove the whole <code>/on/:onDate</code> portion of the path.</p>"
          }
        ],
        "Query Parameters": [
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "country",
            "description": "<p>ISO codes of the countries to be included</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "ccaa",
            "description": "<p>INE codes of the CCAAs to be included</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "state",
            "description": "<p>INE codes of the states to be included</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "city",
            "description": "<p>INE codes of cities to be included</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "localgroup",
            "description": "<p>Code of the Local Group to be included. It represents an alias of one or more filters.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\ndates:\n- 2013-01-01\nvalues:\n- 3197\ncountries:\n  ES:\n    name: España\n    values:\n    - 3197\n    ccaas:\n      '01':\n        name: Andalucia\n        values:\n        - 48\n      '02':\n        name: Aragón\n        values:\n        - 124\n      '03':\n        name: Asturias, Principado de\n        values:\n        - 13\n      '04':\n        name: Baleares, Islas\n        values:\n        - 235\n      '05':\n        name: Canarias\n        values:\n        - 0\n      '06':\n        name: Cantabria\n        values:\n        - 12\n      08:\n        name: Castilla - La Mancha\n        values:\n        - 28\n      '07':\n        name: Castilla y León\n        values:\n        - 24\n      09:\n        name: Cataluña\n        values:\n        - 2054\n      '10':\n        name: Comunidad Valenciana\n        values:\n        - 224\n      '11':\n        name: Extremadura\n        values:\n        - 14\n      '12':\n        name: Galicia\n        values:\n        - 24\n      '13':\n        name: Madrid, Comunidad de\n        values:\n        - 145\n      '14':\n        name: Murcia, Región de\n        values:\n        - 11\n      '15':\n        name: Navarra, Comunidad Foral de\n        values:\n        - 151\n      '16':\n        name: País Vasco\n        values:\n        - 53\n      '17':\n        name: Rioja, La\n        values:\n        - 37",
          "type": "yaml"
        }
      ],
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Date[]",
            "optional": false,
            "field": "dates",
            "description": "<p>Date sequence for all data</p>"
          },
          {
            "group": "Success 200",
            "type": "int[]",
            "optional": false,
            "field": "countries.values",
            "description": "<p>Values aggregated at this level for each date</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "countries",
            "description": "<p>Map indexed by country code</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "countries.name",
            "description": "<p>User visible translated text for CCAA</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "countries.ccaas",
            "description": "<p>Map indexed by CCAA code</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "countries.ccaas.name",
            "description": "<p>User visible translated text for CCAA</p>"
          },
          {
            "group": "Success 200",
            "type": "int[]",
            "optional": false,
            "field": "countries.ccaas.values",
            "description": "<p>Values aggregated at this level for each date</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "countries.ccaas.states",
            "description": "<p>Map indexed by state code</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "countries.ccaas.states.name",
            "description": "<p>User visible translated text for state</p>"
          },
          {
            "group": "Success 200",
            "type": "int[]",
            "optional": false,
            "field": "countries.ccaas.states.values",
            "description": "<p>Values aggregated at this level for each date</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "countries.ccaas.states.cities",
            "description": "<p>Map indexed by city code</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "countries.ccaas.states.cities.name",
            "description": "<p>User visible translated text for city</p>"
          },
          {
            "group": "Success 200",
            "type": "int[]",
            "optional": false,
            "field": "countries.ccaas.states.cities.values",
            "description": "<p>Values aggregated at this level for each date</p>"
          }
        ]
      }
    },
    "filename": "som_opendata/api.py",
    "groupTitle": "Distribution",
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/:metric/by/:geolevel/on/:ondate"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v0.1/contracts/<isodate:fromdate>/monthlyto/<isodate:todate>",
    "title": "Contract Data",
    "version": "0.1.0",
    "name": "Distribution",
    "group": "Distribution",
    "description": "<p>Returns a TSV file with the number of contracts for each city and for each date in the interval.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "isodate",
            "optional": false,
            "field": "fromdate",
            "description": "<p>First date in the output</p>"
          },
          {
            "group": "Parameter",
            "type": "isodate",
            "optional": false,
            "field": "todate",
            "description": "<p>Last included date in the output, if not specified just fromdate is considered</p>"
          }
        ]
      }
    },
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.1/contracts/2015-01-01/monthlyto/2015-12-01"
      }
    ],
    "filename": "som_opendata/oldapi.py",
    "groupTitle": "Distribution"
  },
  {
    "type": "get",
    "url": "/v0.1/members/<isodate:fromdate>[/monthlyto/<isodate:todate>]",
    "title": "Members Data",
    "version": "0.1.0",
    "name": "Distribution",
    "group": "Distribution",
    "description": "<p>Returns a TSV file with the number of members for each city and for each date in the interval.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "isodate",
            "optional": false,
            "field": "fromdate",
            "description": "<p>First date in the output</p>"
          },
          {
            "group": "Parameter",
            "type": "isodate",
            "optional": false,
            "field": "todate",
            "description": "<p>Last included date in the output, if not specified just fromdate is considered</p>"
          }
        ]
      }
    },
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.1/members/2015-01-01/monthlyto/2015-12-01"
      }
    ],
    "filename": "som_opendata/oldapi.py",
    "groupTitle": "Distribution"
  },
  {
    "type": "get",
    "url": "/v0.2/:metric/by/:geolevel/:frequency/from/:fromdate/to/:todate",
    "title": "Metric Data on a Temporal Serie",
    "version": "0.2.15",
    "group": "Distribution",
    "name": "DistributionSeries",
    "description": "<p>Returns the geographical distribution and temporal evolution of a quantity.</p> <p>Use the geolevel to get more geographical detail (country, ccaa, state, city).</p> <p>Use the filters in the query string to restrict to a group of geographical entities. The filters are additive. That means that any city matching any of the specified values will be counted.</p>",
    "examples": [
      {
        "title": "Evolution of all contracts every year",
        "content": "/v0.2/contracts/yearly",
        "type": "json"
      },
      {
        "title": "Monthly evolution of members on 2018",
        "content": "/v0.2/members/monthly/from/2018-01-01/to/2019-01-01",
        "type": "json"
      },
      {
        "title": "2018 monthly evolution of members",
        "content": "/v0.2/members/monthly/from/2018-01-01/to/2019-01-01",
        "type": "json"
      },
      {
        "title": "Members by city on Araba and Gipuzcoa provinces every year",
        "content": "/v0.2/members/by/city/yearly?state=01&state=20",
        "type": "json"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\ndates:\n- 2010-01-01\n- 2011-01-01\n- 2012-01-01\n- 2013-01-01\nvalues:\n- 0\n- 0\n- 277\n- 3197\ncountries:\n  ES:\n    name: España\n    values:\n    - 0\n    - 0\n    - 277\n    - 3197\n    ccaas:\n      '01':\n        name: Andalucia\n        values:\n        - 0\n        - 0\n        - 0\n        - 48\n      '02':\n        name: Aragón\n        values:\n        - 0\n        - 0\n        - 0\n        - 124\n      '03':\n        name: Asturias, Principado de\n        values:\n        - 0\n        - 0\n        - 0\n        - 13\n      '04':\n        name: Baleares, Islas\n        values:\n        - 0\n        - 0\n        - 1\n        - 235\n      '05':\n        name: Canarias\n        values:\n        - 0\n        - 0\n        - 0\n        - 0\n      '06':\n        name: Cantabria\n        values:\n        - 0\n        - 0\n        - 0\n        - 12\n      08:\n        name: Castilla - La Mancha\n        values:\n        - 0\n        - 0\n        - 0\n        - 28\n      '07':\n        name: Castilla y León\n        values:\n        - 0\n        - 0\n        - 0\n        - 24\n      09:\n        name: Cataluña\n        values:\n        - 0\n        - 0\n        - 256\n        - 2054\n      '10':\n        name: Comunidad Valenciana\n        values:\n        - 0\n        - 0\n        - 11\n        - 224\n      '11':\n        name: Extremadura\n        values:\n        - 0\n        - 0\n        - 0\n        - 14\n      '12':\n        name: Galicia\n        values:\n        - 0\n        - 0\n        - 0\n        - 24\n      '13':\n        name: Madrid, Comunidad de\n        values:\n        - 0\n        - 0\n        - 3\n        - 145\n      '14':\n        name: Murcia, Región de\n        values:\n        - 0\n        - 0\n        - 0\n        - 11\n      '15':\n        name: Navarra, Comunidad Foral de\n        values:\n        - 0\n        - 0\n        - 6\n        - 151\n      '16':\n        name: País Vasco\n        values:\n        - 0\n        - 0\n        - 0\n        - 53\n      '17':\n        name: Rioja, La\n        values:\n        - 0\n        - 0\n        - 0\n        - 37",
          "type": "yaml"
        }
      ],
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Date[]",
            "optional": false,
            "field": "dates",
            "description": "<p>Date sequence for all data</p>"
          },
          {
            "group": "Success 200",
            "type": "int[]",
            "optional": false,
            "field": "countries.values",
            "description": "<p>Values aggregated at this level for each date</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "countries",
            "description": "<p>Map indexed by country code</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "countries.name",
            "description": "<p>User visible translated text for CCAA</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "countries.ccaas",
            "description": "<p>Map indexed by CCAA code</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "countries.ccaas.name",
            "description": "<p>User visible translated text for CCAA</p>"
          },
          {
            "group": "Success 200",
            "type": "int[]",
            "optional": false,
            "field": "countries.ccaas.values",
            "description": "<p>Values aggregated at this level for each date</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "countries.ccaas.states",
            "description": "<p>Map indexed by state code</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "countries.ccaas.states.name",
            "description": "<p>User visible translated text for state</p>"
          },
          {
            "group": "Success 200",
            "type": "int[]",
            "optional": false,
            "field": "countries.ccaas.states.values",
            "description": "<p>Values aggregated at this level for each date</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "countries.ccaas.states.cities",
            "description": "<p>Map indexed by city code</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "countries.ccaas.states.cities.name",
            "description": "<p>User visible translated text for city</p>"
          },
          {
            "group": "Success 200",
            "type": "int[]",
            "optional": false,
            "field": "countries.ccaas.states.cities.values",
            "description": "<p>Values aggregated at this level for each date</p>"
          }
        ]
      }
    },
    "filename": "som_opendata/api.py",
    "groupTitle": "Distribution",
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/:metric/by/:geolevel/:frequency/from/:fromdate/to/:todate"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"contracts\"",
              "\"members\"",
              "\"newcontracts\"",
              "\"canceledcontracts\"",
              "\"newmembers\"",
              "\"canceledmember\""
            ],
            "optional": false,
            "field": "metric",
            "description": "<p>Quantity to aggregate</p>"
          },
          {
            "group": "Parameter",
            "type": "Enum",
            "allowedValues": [
              "country",
              "ccaa",
              "state",
              "city"
            ],
            "optional": true,
            "field": "geolevel",
            "defaultValue": "world",
            "description": "<p>Geographical detail level. Use the geolevel to get more geographical detail (country, ccaa, state, city). For just global numbers, remove the whole <code>/by/:geolevel</code> portion of the path.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"yearly\"",
              "\"monthly\""
            ],
            "optional": false,
            "field": "frequency",
            "description": "<p>Indicate a date series (only first day of the month, year...)</p>"
          },
          {
            "group": "Parameter",
            "type": "Date",
            "optional": true,
            "field": "fromdate",
            "defaultValue": "2012-01-01",
            "description": "<p>Earlier date to show, in iso format</p>"
          },
          {
            "group": "Parameter",
            "type": "Date",
            "optional": true,
            "field": "todate",
            "defaultValue": "2020-02-01",
            "description": "<p>Later date to show, in iso format</p>"
          }
        ],
        "Query Parameters": [
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "country",
            "description": "<p>ISO codes of the countries to be included</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "ccaa",
            "description": "<p>INE codes of the CCAAs to be included</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "state",
            "description": "<p>INE codes of the states to be included</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "city",
            "description": "<p>INE codes of cities to be included</p>"
          },
          {
            "group": "Query Parameters",
            "type": "String[]",
            "optional": true,
            "field": "localgroup",
            "description": "<p>Code of the Local Group to be included. It represents an alias of one or more filters.</p>"
          }
        ]
      }
    }
  },
  {
    "type": "get",
    "url": "/v0.2/map/:metric/by/:geolevel/:frequency/from/:fromdate/to/:todate",
    "title": "Absolute Metrics Map Animation",
    "version": "0.2.15",
    "group": "Maps",
    "name": "MapSeries",
    "description": "<p>Returns a map animation that represents the temporal evolution of the geographical distribution.</p> <p>Use the geolevel choose the map detail (ccaa, state). Use the filters in the query string to choose the language. If no language is specified, the language is chosen using the request headers.</p>",
    "examples": [
      {
        "title": "Evolution of all contracts by CCAA every year",
        "content": "/v0.2/map/contracts/by/ccaa/yearly",
        "type": "json"
      },
      {
        "title": "Monthly evolution of members by state on 2018",
        "content": "/v0.2/map/members/by/state/monthly/from/2018-01-01/to/2019-01-01",
        "type": "json"
      },
      {
        "title": "Monthly evolution of members by CCAA from 2018-01-01",
        "content": "/v0.2/map/members/by/ccaa/monthly/from/2018-01-01",
        "type": "json"
      },
      {
        "title": "Members by ccaa every year in Galician",
        "content": "/v0.2/map/members/by/ccaa/yearly?lang=gl",
        "type": "json"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "svg",
            "optional": false,
            "field": "Response",
            "description": "<p>Map animation that represents the temporal evolution of the geographical distribution HTTP/1.1 200 OK</p>"
          }
        ]
      }
    },
    "filename": "som_opendata/api.py",
    "groupTitle": "Maps",
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/map/:metric/by/:geolevel/:frequency/from/:fromdate/to/:todate"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"contracts\"",
              "\"members\"",
              "\"newcontracts\"",
              "\"canceledcontracts\"",
              "\"newmembers\"",
              "\"canceledmember\""
            ],
            "optional": false,
            "field": "metric",
            "description": "<p>Quantity to aggregate</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"ccaa\"",
              "\"state\""
            ],
            "optional": false,
            "field": "geolevel",
            "description": "<p>Geographical detail level</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"yearly\"",
              "\"monthly\""
            ],
            "optional": false,
            "field": "frequency",
            "description": "<p>Indicate a date series (only first day of the month, year...)</p>"
          },
          {
            "group": "Parameter",
            "type": "Date",
            "optional": true,
            "field": "fromdate",
            "defaultValue": "2012-01-01",
            "description": "<p>Earlier date to show, in iso format</p>"
          },
          {
            "group": "Parameter",
            "type": "Date",
            "optional": true,
            "field": "todate",
            "defaultValue": "2020-02-01",
            "description": "<p>Later date to show, in iso format</p>"
          }
        ],
        "Query Parameters": [
          {
            "group": "Query Parameters",
            "type": "String",
            "allowedValues": [
              "\"en\"",
              "\"es\"",
              "\"ca\"",
              "\"gl\"",
              "\"eu\""
            ],
            "optional": true,
            "field": "lang",
            "defaultValue": "browser",
            "description": "<p>defined or en] Forced response language If no language is forced, the one in the browser (Accepted-Language header) is taken. If the languange is not one of the suppoerted, english is taken by default.</p>"
          }
        ]
      }
    }
  },
  {
    "type": "get",
    "url": "/v0.2/map/:metric/per/:relativemetric/by/:geolevel/on/:ondate",
    "title": "Relative Metrics Map",
    "version": "0.2.7",
    "group": "Maps",
    "name": "RelativeMap",
    "description": "<p>Returns a map that represents the relative geographical distribution at a given date.</p> <p>Use the geolevel choose the map detail (ccaa, state). Use the relativemetric to specify the metric to relativize the values by. Use the filters in the query string to choose the language. If no language is specified, the language is chosen using the request headers.</p>",
    "examples": [
      {
        "title": "Current contracts per population by CCAA",
        "content": "/v0.2/map/contracts/per/population/by/ccaa",
        "type": "json"
      },
      {
        "title": "Current members per population by state",
        "content": "/v0.2/map/members/per/population/by/state",
        "type": "json"
      },
      {
        "title": "Members per population by CCAA on 2018-02-01",
        "content": "/v0.2/map/members/per/population/by/ccaa/on/2018-02-01",
        "type": "json"
      },
      {
        "title": "Members per population by ccaa in Galician",
        "content": "/v0.2/map/members/per/population/by/ccaa?lang=gl",
        "type": "json"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "svg",
            "optional": false,
            "field": "Response",
            "description": "<p>Map that represents the relative geographical distribution at a given date</p>"
          }
        ]
      }
    },
    "filename": "som_opendata/api.py",
    "groupTitle": "Maps",
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/map/:metric/per/:relativemetric/by/:geolevel/on/:ondate"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"contracts\"",
              "\"members\"",
              "\"newcontracts\"",
              "\"canceledcontracts\"",
              "\"newmembers\"",
              "\"canceledmember\""
            ],
            "optional": false,
            "field": "metric",
            "description": "<p>Quantity to aggregate</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"population\""
            ],
            "optional": false,
            "field": "relativemetric",
            "description": "<p>Metric to relativize the values by</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"ccaa\"",
              "\"state\""
            ],
            "optional": false,
            "field": "geolevel",
            "description": "<p>Geographical detail level</p>"
          },
          {
            "group": "Parameter",
            "type": "Date",
            "optional": true,
            "field": "ondate",
            "description": "<p>Single date, in ISO format (YYYY-MM-DD). To obtain the last available data, remove the whole <code>/on/:onDate</code> portion of the path.</p>"
          }
        ],
        "Query Parameters": [
          {
            "group": "Query Parameters",
            "type": "String",
            "allowedValues": [
              "\"en\"",
              "\"es\"",
              "\"ca\"",
              "\"gl\"",
              "\"eu\""
            ],
            "optional": true,
            "field": "lang",
            "defaultValue": "browser",
            "description": "<p>defined or en] Forced response language If no language is forced, the one in the browser (Accepted-Language header) is taken. If the languange is not one of the suppoerted, english is taken by default.</p>"
          }
        ]
      }
    }
  },
  {
    "type": "get",
    "url": "/v0.2/map/:metric/per/:relativemetric/by/:geolevel/:frequency/from/:fromdate/to/:todate",
    "title": "Relative Metrics Map Animation",
    "version": "0.2.15",
    "group": "Maps",
    "name": "RelativeMapSeries",
    "description": "<p>Returns a map animation that represents the temporal evolution of the relative geographical distribution.</p> <p>Use the geolevel choose the map detail (ccaa, state). Use the relativemetric to specify the metric to relativize the values by. Use the filters in the query string to choose the language. If no language is specified, the language is chosen using the request headers.</p>",
    "examples": [
      {
        "title": "Evolution of all contracts per population by CCAA every year",
        "content": "/v0.2/map/contracts/per/population/by/ccaa/yearly",
        "type": "json"
      },
      {
        "title": "Monthly evolution of members per population by state on 2018",
        "content": "/v0.2/map/members/per/population/by/state/monthly/from/2018-01-01/to/2019-01-01",
        "type": "json"
      },
      {
        "title": "Monthly evolution of members per population by CCAA from 2018-01-01",
        "content": "/v0.2/map/members/per/population/by/ccaa/monthly/from/2018-01-01",
        "type": "json"
      },
      {
        "title": "Members per population by ccaa every year in Galician",
        "content": "/v0.2/map/members/per/population/by/ccaa/yearly?lang=gl",
        "type": "json"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "svg",
            "optional": false,
            "field": "Response",
            "description": "<p>Map animation that represents the temporal evolution of the geographical distribution HTTP/1.1 200 OK</p>"
          }
        ]
      }
    },
    "filename": "som_opendata/api.py",
    "groupTitle": "Maps",
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/map/:metric/per/:relativemetric/by/:geolevel/:frequency/from/:fromdate/to/:todate"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"contracts\"",
              "\"members\"",
              "\"newcontracts\"",
              "\"canceledcontracts\"",
              "\"newmembers\"",
              "\"canceledmember\""
            ],
            "optional": false,
            "field": "metric",
            "description": "<p>Quantity to aggregate</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"ccaa\"",
              "\"state\""
            ],
            "optional": false,
            "field": "geolevel",
            "description": "<p>Geographical detail level</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"population\""
            ],
            "optional": false,
            "field": "relativemetric",
            "description": "<p>Metric to relativize the values by</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"yearly\"",
              "\"monthly\""
            ],
            "optional": false,
            "field": "frequency",
            "description": "<p>Indicate a date series (only first day of the month, year...)</p>"
          },
          {
            "group": "Parameter",
            "type": "Date",
            "optional": true,
            "field": "fromdate",
            "defaultValue": "2012-01-01",
            "description": "<p>Earlier date to show, in iso format</p>"
          },
          {
            "group": "Parameter",
            "type": "Date",
            "optional": true,
            "field": "todate",
            "defaultValue": "2020-02-01",
            "description": "<p>Later date to show, in iso format</p>"
          }
        ],
        "Query Parameters": [
          {
            "group": "Query Parameters",
            "type": "String",
            "allowedValues": [
              "\"en\"",
              "\"es\"",
              "\"ca\"",
              "\"gl\"",
              "\"eu\""
            ],
            "optional": true,
            "field": "lang",
            "defaultValue": "browser",
            "description": "<p>defined or en] Forced response language If no language is forced, the one in the browser (Accepted-Language header) is taken. If the languange is not one of the suppoerted, english is taken by default.</p>"
          }
        ]
      }
    }
  },
  {
    "type": "get",
    "url": "/v0.2/map/:metric/by/:geolevel/on/:ondate",
    "title": "Absolute Metrics Map",
    "version": "0.2.15",
    "group": "Maps",
    "name": "Static_Map",
    "description": "<p>Returns a map that represents the geographical distribution at a given date.</p> <p>Use the geolevel choose the map detail (ccaa, state).</p>",
    "examples": [
      {
        "title": "Current contracts by CCAA",
        "content": "/v0.2/map/contracts/by/ccaa",
        "type": "json"
      },
      {
        "title": "Members by state on 2018-02-01",
        "content": "/v0.2/map/members/by/state/on/2018-02-01",
        "type": "json"
      },
      {
        "title": "Members by ccaa in Galician",
        "content": "/v0.2/map/members/by/ccaa?lang=gl",
        "type": "json"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"ccaa\"",
              "\"state\""
            ],
            "optional": false,
            "field": "geolevel",
            "description": "<p>Geographical detail level</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"contracts\"",
              "\"members\"",
              "\"newcontracts\"",
              "\"canceledcontracts\"",
              "\"newmembers\"",
              "\"canceledmember\""
            ],
            "optional": false,
            "field": "metric",
            "description": "<p>Quantity to aggregate</p>"
          },
          {
            "group": "Parameter",
            "type": "Date",
            "optional": true,
            "field": "ondate",
            "description": "<p>Single date, in ISO format (YYYY-MM-DD). To obtain the last available data, remove the whole <code>/on/:onDate</code> portion of the path.</p>"
          }
        ],
        "Query Parameters": [
          {
            "group": "Query Parameters",
            "type": "String",
            "allowedValues": [
              "\"en\"",
              "\"es\"",
              "\"ca\"",
              "\"gl\"",
              "\"eu\""
            ],
            "optional": true,
            "field": "lang",
            "defaultValue": "browser",
            "description": "<p>defined or en] Forced response language If no language is forced, the one in the browser (Accepted-Language header) is taken. If the languange is not one of the suppoerted, english is taken by default.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "svg",
            "optional": false,
            "field": "Response",
            "description": "<p>Map that represents the geographical distribution at a given date</p>"
          }
        ]
      }
    },
    "filename": "som_opendata/api.py",
    "groupTitle": "Maps",
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/map/:metric/by/:geolevel/on/:ondate"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v0.2/version",
    "title": "Version information",
    "version": "0.2.15",
    "name": "Version",
    "group": "Version",
    "description": "<p>Response version API</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "version",
            "description": "<p>Current api version</p>"
          },
          {
            "group": "Success 200",
            "optional": false,
            "field": "compat",
            "description": "<p>Oldest backward compatible version</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\nversion: 0.2.15\ncompat: 0.2.1",
          "type": "yaml"
        }
      ]
    },
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/version"
      }
    ],
    "filename": "som_opendata/api.py",
    "groupTitle": "Version"
  },
  {
    "type": "get",
    "url": "/v0.1/version",
    "title": "",
    "version": "0.1.0",
    "name": "Version",
    "group": "Version",
    "description": "<p>Response version API</p>",
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/{version}/version Version Information"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\nversion: 0.1.0\ncompat: 0.1.0",
          "type": "yaml"
        }
      ]
    },
    "filename": "som_opendata/oldapi.py",
    "groupTitle": "Version"
  }
] });
