define({ "api": [
  {
    "type": "get",
    "url": "/v0.2/:field/by/:geolevel/on/:ondate",
    "title": "",
    "version": "0.2.1",
    "group": "Distribution",
    "name": "Distribution",
    "description": "<p>Returns the geographical distribution of a quantity at a given date.</p> <p>Use the geolevel to get more geographical detail (country, ccaa, state, city).</p> <p>Use the filters in the query string to restrict to a group of geographical entities. The filters are additive. That means that any city matching any of the specified values will be counted.</p>",
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
            "field": "field",
            "description": "<p>Field to get.</p>"
          },
          {
            "group": "Parameter",
            "type": "Date",
            "optional": true,
            "field": "ondate",
            "defaultValue": "today",
            "description": "<p>Single date, in iso format.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"country\"",
              "\"ccaa\"",
              "\"state\"",
              "\"city\""
            ],
            "optional": true,
            "field": "geolevel",
            "defaultValue": "world",
            "description": "<p>Geographical detail level</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "country",
            "description": "<p>ISO codes of the countries to be included</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "ccaa",
            "description": "<p>INE codes of the CCAA's to be included</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "state",
            "description": "<p>INE codes of the states to be included</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "city",
            "description": "<p>INE codes of cities to be included</p>"
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
      ]
    },
    "filename": "som_opendata/api.py",
    "groupTitle": "Distribution",
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/:field/by/:geolevel/on/:ondate"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v0.1/contracts/<isodate:fromdate>/monthlyto/<isodate:todate>",
    "title": "",
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
    "title": "",
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
    "url": "/v0.2/:field/by/:geolevel/:frequency/from/:fromdate/to/:todate",
    "title": "",
    "version": "0.2.1",
    "group": "DistributionSeries",
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
            "field": "field",
            "description": "<p>Field to get.</p>"
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
            "description": "<p>Earlier date to show, in iso format.</p>"
          },
          {
            "group": "Parameter",
            "type": "Date",
            "optional": true,
            "field": "todate",
            "defaultValue": "2018-08-01",
            "description": "<p>Later date to show, in iso format.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"country\"",
              "\"ccaa\"",
              "\"state\"",
              "\"city\""
            ],
            "optional": true,
            "field": "geolevel",
            "defaultValue": "world",
            "description": "<p>Geographical detail level</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "country",
            "description": "<p>ISO codes of the countries to be included</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "ccaa",
            "description": "<p>INE codes of the CCAA's to be included</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "state",
            "description": "<p>INE codes of the states to be included</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "city",
            "description": "<p>INE codes of cities to be included</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\ndates:\n- 2010-01-01\n- 2011-01-01\n- 2012-01-01\n- 2013-01-01\nvalues:\n- 0\n- 0\n- 277\n- 3197\ncountries:\n  ES:\n    name: España\n    values:\n    - 0\n    - 0\n    - 277\n    - 3197\n    ccaas:\n      '01':\n        name: Andalucia\n        values:\n        - 0\n        - 0\n        - 0\n        - 48\n      '02':\n        name: Aragón\n        values:\n        - 0\n        - 0\n        - 0\n        - 124\n      '03':\n        name: Asturias, Principado de\n        values:\n        - 0\n        - 0\n        - 0\n        - 13\n      '04':\n        name: Baleares, Islas\n        values:\n        - 0\n        - 0\n        - 1\n        - 235\n      '05':\n        name: Canarias\n        values:\n        - 0\n        - 0\n        - 0\n        - 0\n      '06':\n        name: Cantabria\n        values:\n        - 0\n        - 0\n        - 0\n        - 12\n      08:\n        name: Castilla - La Mancha\n        values:\n        - 0\n        - 0\n        - 0\n        - 28\n      '07':\n        name: Castilla y León\n        values:\n        - 0\n        - 0\n        - 0\n        - 24\n      09:\n        name: Cataluña\n        values:\n        - 0\n        - 0\n        - 256\n        - 2054\n      '10':\n        name: Comunidad Valenciana\n        values:\n        - 0\n        - 0\n        - 11\n        - 224\n      '11':\n        name: Extremadura\n        values:\n        - 0\n        - 0\n        - 0\n        - 14\n      '12':\n        name: Galicia\n        values:\n        - 0\n        - 0\n        - 0\n        - 24\n      '13':\n        name: Madrid, Comunidad de\n        values:\n        - 0\n        - 0\n        - 3\n        - 145\n      '14':\n        name: Murcia, Región de\n        values:\n        - 0\n        - 0\n        - 0\n        - 11\n      '15':\n        name: Navarra, Comunidad Foral de\n        values:\n        - 0\n        - 0\n        - 6\n        - 151\n      '16':\n        name: País Vasco\n        values:\n        - 0\n        - 0\n        - 0\n        - 53\n      '17':\n        name: Rioja, La\n        values:\n        - 0\n        - 0\n        - 0\n        - 37",
          "type": "yaml"
        }
      ]
    },
    "filename": "som_opendata/api.py",
    "groupTitle": "DistributionSeries",
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/:field/by/:geolevel/:frequency/from/:fromdate/to/:todate"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v0.2/version",
    "title": "",
    "version": "0.2.1",
    "name": "Version",
    "group": "Version",
    "description": "<p>Response version API</p>",
    "sampleRequest": [
      {
        "url": "https://opendata.somenergia.coop/v0.2/version"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\nversion: 0.2.1\ncompat: 0.2.0",
          "type": "yaml"
        }
      ]
    },
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
        "url": "https://opendata.somenergia.coop/{version}/version"
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
