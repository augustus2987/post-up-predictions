from sportsreference.nfl.teams import Teams
from sportsreference.nfl.schedule import Schedule

schedule2020 = Schedule('DEN', year='2020')

teams2020 = Teams(year='2020')

for game in schedule2020:
    print(game.dataframe)