from werkzeug.exceptions import HTTPException
from yamlns import namespace as ns
from consolemsg import u

class MissingDateError(HTTPException):

    missingDates = []
    code = 500

    def __init__(self, missingDates):
        super(MissingDateError, self).__init__("Missing Dates " + u(missingDates))
        self.missingDates = missingDates


class ValidateError(HTTPException):

    valors = ns(
        metric=['members', 'contracts'],
        frequency=['monthly', 'yearly'],
        geolevel=['country', 'ccaa', 'state', 'city']
        )

    code = 400

    parameter = ''
    value = ''
    possibleValues = []

    def __init__(self, field, value):
        self.parameter = field
        self.value = value
        self.possibleValues = self.valors[field]
        super(ValidateError, self).__init__("Incorrect "+field+" \'"+value+
            "\' try with "+u(self.possibleValues)
            )
