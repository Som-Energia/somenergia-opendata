
class MissingDateError(Exception):

    missingDates = []

    def __init__(self, missingDates):
        super(MissingDateError, self).__init__("Error chungo")
        self.missingDates = missingDates
