from . import constants

class urlMapper:
    @staticmethod
    def Map(locationNumber):
        if locationNumber in [2, 3, 4, 5, 6]:
            return constants.CITY_COMMUNITY_TENNIS_URL
        elif locationNumber in [55, 72]:
            return constants.PARKLANDS_URL
        elif locationNumber == 43:
            return constants.LANGHAM_HOTEL_URL
        elif locationNumber == 70:
            return constants.CAMPERDOWN_URL
        elif locationNumber == 100:
            return constants.FULLAGAR_URL