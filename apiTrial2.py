from pandas.core.algorithms import diff
from sportsreference.nba.schedule import Schedule
from sportsreference.nba.boxscore import Boxscore
import pandas as pd
import numpy as np

class NBA_Data:

    # Note 2020 Corresponds to the 2019-2020 season, 2021 corresponds to 2020-2021 season


    def __init__(self, team, year=2019, last_game=82, game_recency=5):

        self.year = year 
        self.team = team

        self.game_recency = game_recency
        self.last_game = last_game


        # Get schedule objects

        print("Fetching ", self.team, " schedule")

        self.team_schedule = self.get_schedule(team)

        print()
        print(self.team_schedule.dataframe.to_string())
        print()

        # Store list of opponent abbreviations
        # Store list of wins or losses (Win = 1, Loss = 0)
        # Store list of if game was home or away
        # Store list of boxscore indices

        self.opponents = []         # EX: 'MIA'
        self.results = []           # Win = 1, Loss = 0
        self.home_or_away = []      # 'Home' or 'Away'
        self.boxscore_ind = []
        self.games_statistics = []

        for i, game in enumerate(self.team_schedule):

            if i >= last_game:
                break

            if game.dataframe["playoffs"].iloc[0]: # don't inlcude playoffs
                continue
            
            self.opponents.append(game.dataframe["opponent_abbr"].iloc[0])
            self.boxscore_ind.append(game.dataframe["boxscore_index"].iloc[0])
            self.home_or_away.append(game.dataframe["location"].iloc[0])

            print("Fetching Game: ", i+1, " (", game.dataframe["boxscore_index"].iloc[0], ")")
        
            self.games_statistics.append( Boxscore( game.dataframe["boxscore_index"].iloc[0] ).dataframe.iloc[0] )
            
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

    def get_recent_game_data(self, game_num):
        
        # Get the last boxscore indices for the recent games before specified game

        games_to_consider = []
        indices = []

        for i, game in enumerate(self.boxscore_ind):

            if (i+1) < game_num and (i+1) >= game_num - self.game_recency:
                games_to_consider.append(game)
                indices.append(i)


        # Get the data of the games from boxscores

        game_data_list = []

        for i in range(len(games_to_consider)): # emulating: for "game"
             
            index = indices[i]

            #game_data_temp = Boxscore(str(games_to_consider[i])).dataframe.iloc[0]
            game_data_temp = self.games_statistics[i]
            
            game_stats = []

            if self.home_or_away[index] == 'Home': # Need to pull home data      
                
                for stat_name in self.home_feature_names:

                    temp = game_data_temp[stat_name]

                    if temp is None:
                        temp = 0
                    game_stats.append(temp)
                    

            else: # Need to pull away data

                for stat_name in self.away_feature_names:

                    temp = game_data_temp[stat_name]
                    if temp is None:
                        temp = 0
                    
                    game_stats.append(temp)

            game_data_list.append(game_stats)
        
        game_data_list = np.asarray(game_data_list).astype(np.float64)


        # Now we need to get opponents game data

        target_game = self.boxscore_ind[game_num-1]
        opp = self.opponents[game_num-1]

        opp_average = self.get_opp_game_data(opp, target_game)

        team_average = np.average(game_data_list, axis=0)

        print("OPP AVERAGE OVER PREVIOUS ", str(self.game_recency), " GAMES:")
        print(opp_average)
        print() 

        print("TEAM AVERAGE OVER PREVIOUS ", str(self.game_recency), " GAMES:")
        print(team_average)
        print()

        diff_vector = np.subtract(team_average, opp_average)

        print("DIFFERENCE VECTOR: ")
        print(diff_vector)
        print()

        label = self.results[game_num-1]
        print("LABEL")
        print(label)

        return diff_vector, label


    def get_opp_game_data(self, opp, target_game):

        opp_sched = self.get_schedule(opp)

        boxscore_ind = []
        home_or_away = []

        for i, game in enumerate(opp_sched):

            found = i
            

            if game.dataframe["boxscore_index"].iloc[0] == target_game:
                break

            boxscore_ind.append(game.dataframe["boxscore_index"].iloc[0])
            home_or_away.append(game.dataframe["location"].iloc[0])


        boxscore_ind = boxscore_ind[found-self.game_recency:found] # This is the opponents last [5] games (by boxscore index)
        home_or_away = home_or_away[found-self.game_recency:found] # ^^ (by Home or Away)

        # Games have been found! 

        # Now we need to get the actual data from the specified games

        game_data_list = []

        for i in range(len(boxscore_ind)):
            
            game_stats = []

            print("Fetching game for ", opp, " ( ", str(boxscore_ind[i]), " )")
            game_data_temp = Boxscore(str(boxscore_ind[i])).dataframe.iloc[0]

            if home_or_away[i] == 'Home': # Need to pull home data      
                
                for stat_name in self.home_feature_names:

                    temp = game_data_temp[stat_name]

                    if temp is None:
                        temp = 0

                    game_stats.append(temp)
                    

            else: # Need to pull away data

                for stat_name in self.away_feature_names:

                    temp = game_data_temp[stat_name]

                    if temp is None:
                        temp = 0

                    game_stats.append(temp)

            game_data_list.append(np.asarray(game_stats))


        to_return = np.asarray(game_data_list).astype(np.float64)

        print()

        return np.average(to_return, axis=0)

    def generate_data(self):

        X = []
        y = []

        for i in range(self.game_recency, self.last_game):

            X_item, y_item = self.get_recent_game_data(i)
            X.append(X_item)
            y.append(y_item)

        print("Finished")

        return X, y


        
            




denver_obj = NBA_Data('DEN', last_game=32, game_recency=5)
denver_obj.generate_data()
#denver_obj.get_recent_game_data(10)
