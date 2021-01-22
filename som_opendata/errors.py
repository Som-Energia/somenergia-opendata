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
        # TODO: Construct this from source metadata
        metric=[
            'members',
            'contracts',
            'newcontracts',
            'canceledcontracts',
            'newmembers',
            'canceledmembers',
            ],
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
        super(ValidateError, self).__init__(
            "Incorrect {} '{}' try with {}".format(
                field, value, u(self.possibleValues))
            )

class AliasNotFoundError(HTTPException):
    code = 400
    def __init__(self, alias, value):
        super(AliasNotFoundError, self).__init__(
            "{} '{}' not found".format(alias, value))


