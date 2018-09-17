from werkzeug.exceptions import HTTPException
from yamlns import namespace as ns


class MissingDateError(HTTPException):

    missingDates = []
    code = 500
    errorId = 1001

    def __init__(self, missingDates):
        super(MissingDateError, self).__init__("Missing Dates " + str(missingDates))
        self.missingDates = missingDates


class ValidateError(HTTPException):

    valors = ns(metric=['members', 'contracts'],
        frequency=['monthly', 'yearly'],
        geolevel=['country', 'ccaa', 'state', 'city']
        )

    code = 400
    errorId = 0

    typeErrors = ns(metric=1002, frequency=1003, geolevel=1004)

    def __init__(self, typeError, value):
        self.errorId = self.typeErrors[typeError]
        super(ValidateError, self).__init__("Incorrect "+typeError+" \'"+value+
            "\' try with "+str(self.valors[typeError])
            )
