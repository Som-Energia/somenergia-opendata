from werkzeug.exceptions import HTTPException
from yamlns import namespace as ns


class MissingDateError(HTTPException):

    missingDates = []
    code = 500

    def __init__(self, missingDates):
        super(MissingDateError, self).__init__("Missing Dates " + str(missingDates))
        self.missingDates = missingDates


class ValidateError(HTTPException):

    valors = ns(metric=['members', 'contracts'],
        frequency=['monthly', 'yearly'],
        geolevel=['country', 'ccaa', 'state', 'city']
        )

    code = 400

    metric = ''
    value = ''
    possibleValues = []

    def __init__(self, typeError, value):
        self.metric = typeError
        self.value = value
        self.possibleValues = self.valors[typeError]
        super(ValidateError, self).__init__("Incorrect "+typeError+" \'"+value+
            "\' try with "+str(self.possibleValues)
            )
