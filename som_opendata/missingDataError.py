


class MissingDataError(Exception):

    data = []
    missedDates = []
    missedLocations = []
    existCounts = []
    # existCities es suposa que serien totes

    def __init__(self, data, missedDates, missedLocations):
        self.data = data
        self.missedDates = missedDates
        self.missedLocations = missedLocations

    