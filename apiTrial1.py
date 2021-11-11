from sportsreference.nba.teams import Teams
from sportsreference.nba.schedule import Schedule
from sportsreference.nba.boxscore import Boxscore

# schle202edu0 = Schedule('DEN', year='2020')

# teams2020 = Teams(year='2020')

# for game in schedule2020:
#     print(game.dataframe)



class NBA_Format:
    def __init__(self, year=2020):
        self.year = year 

    def get_team_schedule(self, team='DEN'):
        try:
            return Schedule('DEN', year=str(self.year))
        except:
            print('Error')
            return -1

    def format_schedule(self, sched, game_num, games_before='all'):

        to_return = []

        if(games_before == 'all'):

            for i, game in enumerate(sched):   
                if (i+1) < game_num:
                    #to_return.append(game.dataframe["boxscore_index"])
                    to_return.append(game.dataframe['boxscore_index'][0])
                else:
                    break
        else:

            for i, game in enumerate((sched)):
                if (i+1) < game_num and (i+1) >= game_num - games_before:
                    to_return.append(game.dataframe['boxscore_index'][0])

        return to_return

    def get_game_data(self, boxscores_lst):

        to_return = []

        for boxscore in boxscores_lst:
            to_return.append( Boxscore(str(boxscore)).dataframe )

        return to_return


n = NBA_Format()
s = n.get_team_schedule()
res = n.format_schedule(s, 5)
data= n.get_game_data(res)

for d in data:
    print(d)
