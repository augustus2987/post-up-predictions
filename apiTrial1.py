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
# Input4: train on the whole season up to a given game or 
class NBA_Data:
    def __init__(self, team1, team2, year=2020, train_type="all"):
        self.year = year 
        self.train_type = train_type

        self.team1 = team1
        self.team1_schedule = [] # list of boxscore indices
        self.team1_data = []

        self.team2 = team2
        self.team2_schedule = [] # list of boxscore indices
        self.team2_data = []

        self.features_names = ['away_defensive_rebound_percentage', 'away_effective_field_goal_percentage', 'away_offensive_rebound_percentage', 'away_offensive_rating',
        'home_defensive_rebound_percentage', 'home_effective_field_goal_percentage', 'home_offensive_rebound_percentage', 'home_offensive_rating']
        self.home_features 


    # Set the schedule for the teams.
    def get_team_schedules(self):
        try:
            team1_sch = Schedule(self.team1, year=str(self.year))
            team2_sch = Schedule(self.team2, year=str(self.year))
        except:
            print('Error')
            return -1
        
        for game in team1_sch:
            self.team1_schedule.append(game.dataframe['boxscore_index'][0])
        for game in team2_sch:
            self.team2_schedule.append(game.dataframe['boxscore_index'][0])


    # DEPRECATED 
    # Return the boxscore nubmer (uid) for each game in specified range
    # Input1 teamname string abbreviation 
    # Input2 last game number in season to include
    # Input3 number of games to include in output (default is all games of a season)
    def get_boxscores(self, team, game_num, games_before='all'):
        boxscore_indices = [] 

        try:
            schedule = Schedule(team, year=str(self.year))
        except:
            print('ERROR')
            return -1

        # get boxscores from games in schedule.
        if(games_before == 'all'): # whole season
            for i, game in enumerate(schedule):   
                if (i+1) < game_num:
                    #to_return.append(game.dataframe["boxscore_index"])
                    boxscore_indices.append(game.dataframe['boxscore_index'][0])
                else:
                    break
        else:
            for i, game in enumerate(schedule):
                if (i+1) < game_num and (i+1) >= game_num - games_before:
                    boxscore_indices.append(game.dataframe['boxscore_index'][0])

        return boxscore_indices



    # Take a list of boxscore indices of games and output the stats from each game. 
    # Input1: list of strings of feature names 
    def get_game_data(self, features_names=None):
    
        for boxscore in self.team1_schedule:
            gamedata = Boxscore(str(boxscore)).dataframe
            self.team1_data.append(gamedata.loc[:,self.features_names].values) # turn into nparray

        for boxscore in self.team2_schedule:
            gamedata = Boxscore(str(boxscore)).dataframe
            self.team2_data.append(gamedata.loc[:,self.features_names].values) # turn into nparray

s = Schedule('DEN', '2019')
bs = []
gd = []
for game in s:
    bs.append(game.dataframe['boxscore_index'][0])
print(bs)
for i, boxscore in enumerate(bs):
    gamedata = Boxscore(str(boxscore)).dataframe
    gd.append(gamedata.values)
    print(i)
    print(gamedata)
# print(Boxscore('201810170LAC').dataframe)
# nbad = NBA_Data('DEN', 'LAC', 2019)
# nbad.get_team_schedules()
# nbad.get_game_data()
# print(nbad.team1_data)