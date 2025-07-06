from .constants import constants

class urlMapper:
    @staticmethod
    def Map(locationNumber):
        if locationNumber == 2 or 3 or 4 or 5 or 6:
            return constants.CITY_COMMUNITY_TENNIS_URL
        elif locationNumber == 55 or 72:
            return constants.PARKLANDS_URL
        elif locationNumber == 43:
            return constants.LANGHAM_HOTEL_URL
        elif locationNumber == 70:
            return constants.CAMPERDOWN_URL