from sportsreference.nba.schedule import Schedule
from sportsreference.nba.boxscore import Boxscore
import pandas as pd
import numpy as np

class NBA_Data:

    def __init__(self, team, year=2020):

        self.year = year 
        self.team = team


        # Get schedule objects

        self.team_schedule = self.get_schedule(team)

        # Store list of opponent abbreviations
        # Store list of wins or losses (Win = 1, Loss = 0)
        # Store list of if game was home or away
        # Store list of boxscore indices

        self.opponents = []         # EX: 'MIA'
        self.results = []           # Win = 1, Loss = 0
        self.home_or_away = []      # 'Home' or 'Away'
        self.boxscore_ind = []

        for game in self.team_schedule:

            if game.dataframe["playoffs"].iloc[0]: # don't inlcude playoffs
                continue
            
            self.opponents.append(game.dataframe["opponent_abbr"].iloc[0])
            self.boxscore_ind.append(game.dataframe["boxscore_index"].iloc[0])
            self.home_or_away.append(game.dataframe["location"].iloc[0])
            
            if game.dataframe["result"].iloc[0] == "Win":
                self.results.append(1)
            else:
                self.results.append(0)

        self.features_names = [
            'assist_percentage',
            'assists',	
            'block_percentage',	
            'blocks',
            'defensive_rating',	
            'defensive_rebound_percentage',	
            'defensive_rebounds',	
            'effective_field_goal_percentage',	
            'field_goal_attempts',	
            'field_goal_percentage',	
            'field_goals',	
            'free_throw_attempt_rate',	
            'free_throw_attempts',	
            'free_throw_percentage',	
            'free_throws',	
            'minutes_played',	
            'offensive_rating',	
            'offensive_rebound_percentage',	
            'offensive_rebounds',
            'personal_fouls',	
            'points',	
            'steal_percentage',	
            'steals',	
            'three_point_attempt_rate',	
            'three_point_field_goal_attempts',	
            'three_point_field_goal_percentage',	
            'three_point_field_goals',	
            'total_rebound_percentage',	
            'total_rebounds',	
            'true_shooting_percentage',	
            'turnover_percentage',	
            'turnovers',	
            'two_point_field_goal_attempts',	
            'two_point_field_goal_percentage',	
            'two_point_field_goals',	
        ]
        self.home_feature_names = ['home_' + stat for stat in self.features_names]
        self.away_feature_names = ['away_' + stat for stat in self.features_names]

    def get_schedule(self, team):

        return Schedule(team, year=str(self.year))

    def get_recent_game_data(self, game_num, game_recency = 5):
        
        # Get the last boxscore indices for the recent games before specified game

        games_to_consider = []
        indices = []

        for i, game in enumerate(self.boxscore_ind):

            if (i+1) < game_num and (i+1) >= game_num - game_recency:
                games_to_consider.append(game)
                indices.append(i)


        # Get the data of the games from boxscores

        game_data_list = []

        for i in range(len(games_to_consider)):
            
            index = indices[i]

            game_data_temp = Boxscore(str(games_to_consider[i])).dataframe.iloc[0]
            
            game_stats = []

            if self.home_or_away[index] == 'Home': # Need to pull home data      
                
                for stat_name in self.home_feature_names:
                    game_stats.append(game_data_temp[stat_name])
                    

            else: # Need to pull away data

                for stat_name in self.away_feature_names:
                    game_stats.append(game_data_temp[stat_name])

            game_data_list.append(game_stats)

            print("GAME DATA BABY")
            print(game_stats)
            print()
            print()



            

        #return i, games_to_consider

    def boxscore_ind_to_data(self, boxscore_ind_lst):

        to_return = []

        for boxscore in boxscore_ind_lst:

            game_data = Boxscore(str(boxscore)).dataframe

    def get_game_data_final(self, game_num, game_recency = 5):

        index_lst, game_data = self.get_recent_game_data(game_num)
            




denver_obj = NBA_Data('DEN')
denver_obj.get_recent_game_data(10)
