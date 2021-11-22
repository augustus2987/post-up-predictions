# from sportsreference.nba.teams import Teams
from sportsreference.nba.schedule import Schedule
from sportsreference.nba.boxscore import Boxscore
import pandas as pd
import numpy as np

# schle202edu0 = Schedule('DEN', year='2020')

# teams2020 = Teams(year='2020')

# for game in schedule2020:
#     print(game.dataframe)


# Class for formatting NBA DATA 
# Input1: team 1 name string abbreviation
# Input2: team 2 name string abbreviation
# Input3: season year default 2020
class NBA_Data:
    def __init__(self, team1, team2, year=2020, ):
        self.year = year 
        self.team1 = team1
        self.team2 = team2
        # self.team1_schedule = None
        # self.team2_schedule = None
        self.features_names = ['away_defensive_rebound_percentage', 'away_effective_field_goal_percentage', 'away_offensive_rebound_percentage', 'away_offensive_rating',
        'home_defensive_rebound_percentage', 'home_effective_field_goal_percentage', 'home_offensive_rebound_percentage', 'home_offensive_rating']

    ### DEPRECATED ###
    # Return the schedule for a team for the given year. 
    # Input1: Team name string abbreviation
    def get_team_schedule(self, team='DEN'):
        try:
            return Schedule(team, year=str(self.year))
        except:
            print('Error')
            return -1


    # Return the boxscore nubmer (uid) for each game in specified range
    # Input1 teamname string abbreviation 
    # Input2 last game number in season to include
    # Input3 number of games to include in output (default is all games of a season)
    def get_boxscores(self, team, game_num, games_before='all'):
        boxscore_indicies = [] 

        # get schedule
        try:
            schedule = Schedule(team, year=str(self.year))
        except:
            print('Error')
            return -1

        # get boxscores from games in schedule.
        if(games_before == 'all'): # whole season
            for i, game in enumerate(schedule):   
                if (i+1) < game_num:
                    #to_return.append(game.dataframe["boxscore_index"])
                    boxscore_indicies.append(game.dataframe['boxscore_index'][0])
                else:
                    break
        else:
            for i, game in enumerate(schedule):
                if (i+1) < game_num and (i+1) >= game_num - games_before:
                    boxscore_indicies.append(game.dataframe['boxscore_index'][0])

        return boxscore_indicies

    # Take a list of boxscore indexes of games and output the stats from each game. 
    # Input1: list of boxscore indexes
    # output a list of games (each of type pandas dataframe)
    def get_game_data(self, boxscores_lst):

        to_return = []

        for boxscore in boxscores_lst:
            gamedata = Boxscore(str(boxscore)).dataframe
            to_return.append(gamedata.loc[:,self.features_names].values) # turn into nparray
        return to_return


nba = NBA_Data('DEN', 'LAC', 2020)
res = nba.get_boxscores(nba.team1, 2, 'all')
data= nba.get_game_data(res)

print(nba.features_names)
print(data)



# print(type(res)) # list of game indexes 
# print(type(data)) # list of game dataframes
# print(type(data[0])) # dataframe 
# print(type(data[0]['away_assist_percentage'])) # pandas series

# for d in data[0]:
#     print(d)