class CourtMapper:
    @staticmethod
    def Map(courtNumber):
            
            courtOne = [279,281,139,283]
            courtTwo = [280,282,140]
            courtFive = 227

            if(courtNumber in courtOne):
                return 1
            elif(courtNumber in courtTwo):
                return 2
            elif(courtNumber == courtFive):
                return 5    
            else:
                return courtNumber