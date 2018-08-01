


class MissingDataError(Exception):

    data = []
    missedDates = []
    missedLocations = []

    def __init__(self, data, missedDates, missedLocations):
        self.data = data
        self.missedDates = missedDates
        self.missedLocations = missedLocations

    