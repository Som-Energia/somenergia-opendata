define({ "api": [
  {
    "type": "get",
    "url": "/printer/:field[/by/:aggregateLevel]/on/:ondate|/frequency/:frequency[/from/:fromdate][/to/:todate]?queryFilter=:locationFilters",
    "title": "",
    "version": "1.0.1",
    "name": "OpenData",
    "group": "Printer",
    "description": "<p>Retorna un yaml amb la distribució desitjada repartida en espai - temps</p>",
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
            "description": "<p>Firstname of the User.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "ondate",
            "description": "<p>Date in iso format.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "fromdate",
            "defaultValue": "2012-01-01",
            "description": "<p>Date in iso format.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "todate",
            "defaultValue": "2018-08-01",
            "description": "<p>Date in iso format.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"countries\"",
              "\"ccaas\"",
              "\"states\"",
              "\"cities\""
            ],
            "optional": true,
            "field": "aggregateLevel",
            "defaultValue": "world",
            "description": "<p>Aggregate level response.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"yearly\"",
              "\"monthly\""
            ],
            "optional": true,
            "field": "frequency",
            "description": "<p>Frequency response.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "allowedValues": [
              "\"contry\"",
              "\"ccaa\"",
              "\"state\"",
              "\"city\""
            ],
            "optional": true,
            "field": "queryFilter",
            "description": "<p>Query Geographical filter.</p>"
          }
        ]
      }
    },
    "sampleRequest": [
      {
        "url": "http://192.168.1.5:5001/printer/contracts/by/ccaas/yearly/from/2010-01-01/to/2013-01-01?country=ES"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\n{\n    dates:\n    - 2010-01-01\n    - 2011-01-01\n    - 2012-01-01\n    - 2013-01-01\n    data:\n    - 0\n    - 0\n    - 277\n    - 3197\n    countries:\n      ES:\n        name: España\n        data:\n        - 0\n        - 0\n        - 277\n        - 3197\n        ccaas:\n          '01':\n            name: Andalucia\n            data:\n            - 0\n            - 0\n            - 0\n            - 48\n          '02':\n            name: Aragón\n            data:\n            - 0\n            - 0\n            - 0\n            - 124\n          '03':\n            name: Asturias, Principado de\n            data:\n            - 0\n            - 0\n            - 0\n            - 13\n          '04':\n            name: Baleares, Islas\n            data:\n            - 0\n            - 0\n            - 1\n            - 235\n          '05':\n            name: Canarias\n            data:\n            - 0\n            - 0\n            - 0\n            - 0\n          '06':\n            name: Cantabria\n            data:\n            - 0\n            - 0\n            - 0\n            - 12\n          08:\n            name: Castilla - La Mancha\n            data:\n            - 0\n            - 0\n            - 0\n            - 28\n          '07':\n            name: Castilla y León\n            data:\n            - 0\n            - 0\n            - 0\n            - 24\n          09:\n            name: Cataluña\n            data:\n            - 0\n            - 0\n            - 256\n            - 2054\n          '10':\n            name: Comunidad Valenciana\n            data:\n            - 0\n            - 0\n            - 11\n            - 224\n          '11':\n            name: Extremadura\n            data:\n            - 0\n            - 0\n            - 0\n            - 14\n          '12':\n            name: Galicia\n            data:\n            - 0\n            - 0\n            - 0\n            - 24\n          '13':\n            name: Madrid, Comunidad de\n            data:\n            - 0\n            - 0\n            - 3\n            - 145\n          '14':\n            name: Murcia, Región de\n            data:\n            - 0\n            - 0\n            - 0\n            - 11\n          '15':\n            name: Navarra, Comunidad Foral de\n            data:\n            - 0\n            - 0\n            - 6\n            - 151\n          '16':\n            name: País Vasco\n            data:\n            - 0\n            - 0\n            - 0\n            - 53\n          '17':\n            name: Rioja, La\n            data:\n            - 0\n            - 0\n            - 0\n            - 37\n}",
          "type": "yaml"
        }
      ]
    },
    "filename": "som_opendata/printer/printer.py",
    "groupTitle": "Printer"
  }
] });
