define({ "api": [
  {
    "type": "get",
    "url": "/old/contracts/<isodate:fromdate>/monthlyto/<isodate:todate>",
    "title": "",
    "version": "1.0.1",
    "name": "Contracts",
    "group": "Contracts",
    "description": "<p>Retorna un fitxer yaml amb els contractes de cada pais-ccaa-provincia-municipi</p>",
    "sampleRequest": [
      {
        "url": "http://DNS-NAME:5001/old/contracts/2015-01-01/monthlyto/2015-12-01"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\n{\n    dates: \n        - 2018-01-01\n        level: countries\n        countries:\n          ES:\n            name: España\n            data: [2020]\n            ccaas:\n              '09':\n                name: Catalunya\n                data: [2020]\n                states:\n                  '17':\n                    name: Girona\n                    data: [2020]\n}",
          "type": "yaml"
        }
      ]
    },
    "filename": "./som_opendata/api.py",
    "groupTitle": "Contracts"
  },
  {
    "type": "get",
    "url": "/old/members/<isodate:fromdate>/monthlyto/<isodate:todate>",
    "title": "",
    "version": "1.0.1",
    "name": "Members",
    "group": "Members",
    "description": "<p>Retorna un fitxer yaml amb els socis de cada pais-ccaa-provincia-municipi</p>",
    "sampleRequest": [
      {
        "url": "http://DNS-NAME:5001/old/members/2015-01-01/monthlyto/2015-12-01"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\n{\n    dates: \n        - 2018-01-01\n        level: countries\n        countries:\n          ES:\n            name: España\n            data: [2020]\n            ccaas:\n              '09':\n                name: Catalunya\n                data: [2020]\n                states:\n                  '17':\n                    name: Girona\n                    data: [2020]\n}",
          "type": "yaml"
        }
      ]
    },
    "filename": "./som_opendata/api.py",
    "groupTitle": "Members"
  },
  {
    "type": "get",
    "url": "/socis/<country:pais>/<int:ccaa>",
    "title": "",
    "version": "1.0.1",
    "name": "Socis_CCAA",
    "group": "Socis",
    "description": "<p>Retorna els socis que hi ha en una CCAA d'un pais</p>",
    "sampleRequest": [
      {
        "url": "http://DNS-NAME:5001/socis/ES/09"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\n{\n    socis: 8800\n}",
          "type": "yaml"
        }
      ]
    },
    "filename": "./som_opendata/socis/socis.py",
    "groupTitle": "Socis"
  },
  {
    "type": "get",
    "url": "/socis/<country:pais>/<int:ccaa>/<int:provincia>",
    "title": "",
    "version": "1.0.1",
    "name": "Socis_CCAA",
    "group": "Socis",
    "description": "<p>Retorna els socis que hi ha en una provincia d'una CCAA d'un pais</p>",
    "sampleRequest": [
      {
        "url": "http://DNS-NAME:5001/socis/ES/09/17"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\n{\n    socis: 880\n}",
          "type": "yaml"
        }
      ]
    },
    "filename": "./som_opendata/socis/socis.py",
    "groupTitle": "Socis"
  },
  {
    "type": "get",
    "url": "/socis/<country:pais>/<int:ccaa>/<int:provincia>/<int:ine>",
    "title": "",
    "version": "1.0.1",
    "name": "Socis_CCAA",
    "group": "Socis",
    "description": "<p>Retorna els socis que hi ha en un municipi d'una provincia d'una CCAA d'un pais</p>",
    "sampleRequest": [
      {
        "url": "http://DNS-NAME:5001/socis/ES/09/17/17079"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\n{\n    socis: 88\n}",
          "type": "yaml"
        }
      ]
    },
    "filename": "./som_opendata/socis/socis.py",
    "groupTitle": "Socis"
  },
  {
    "type": "get",
    "url": "/socis/<country:pais>",
    "title": "",
    "version": "1.0.1",
    "name": "Socis_Country",
    "group": "Socis",
    "description": "<p>Retorna els socis que hi ha en el pais</p>",
    "sampleRequest": [
      {
        "url": "http://DNS-NAME:5001/socis/ES"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\n{\n    socis: 88000\n}",
          "type": "yaml"
        }
      ]
    },
    "filename": "./som_opendata/socis/socis.py",
    "groupTitle": "Socis"
  },
  {
    "type": "get",
    "url": "/old/version",
    "title": "",
    "version": "1.0.1",
    "name": "Version",
    "group": "Version",
    "description": "<p>Response version API</p>",
    "sampleRequest": [
      {
        "url": "http://DNS-NAME:5001/old/version"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200OK\n{\n    version: 1.0\n}",
          "type": "yaml"
        }
      ]
    },
    "filename": "./som_opendata/api.py",
    "groupTitle": "Version"
  },
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./doc/main.js",
    "group": "_home_usuari_Projectes_somenergia_api_doc_main_js",
    "groupTitle": "_home_usuari_Projectes_somenergia_api_doc_main_js",
    "name": ""
  }
] });
