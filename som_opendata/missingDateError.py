from werkzeug.exceptions import HTTPException
from yamlns import namespace as ns


class MissingDateError(HTTPException):

    missingDates = []
    code = 500
    errorId = 1001

    def __init__(self, missingDates):
        super(MissingDateError, self).__init__("Missing Dates " + str(missingDates))
        self.missingDates = missingDates
