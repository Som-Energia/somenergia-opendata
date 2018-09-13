from werkzeug.exceptions import HTTPException
from yamlns import namespace as ns


class MissingDateError(HTTPException):

    missingDates = []
    code = 500
    errorId = 1001

    def __init__(self, missingDates):
        super(MissingDateError, self).__init__("Missing Dates " + str(missingDates))
        self.missingDates = missingDates


class MetricValidateError(HTTPException):

    correctMetrics = ['members', 'contracts']
    code = 400
    errorId = 1002

    def __init__(self, metric):
        super(MetricValidateError, self).__init__("Incorrect metric \'"+metric+
            "\' try with "+str(self.correctMetrics)
            )


class FrequencyValidateError(HTTPException):

    correctFrequency = ['monthly', 'yearly']
    code = 400
    errorId = 1003

    def __init__(self, frequency):
        super(FrequencyValidateError, self).__init__("Incorrect frequency \'"+frequency+
            "\' try with "+str(self.correctFrequency)
            )