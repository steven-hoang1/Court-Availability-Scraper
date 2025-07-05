from TennisCourtScraper import TennisCourtScraper

CityCommunityTennisUrl = "https://jensenstennis.intrac.com.au/tennis/book.cfm?location="
ParklandsUrl = "https://parklands.intrac.com.au/sports/schedule.cfm?location="

results = TennisCourtScraper.scrape(ParklandsUrl, 72)


