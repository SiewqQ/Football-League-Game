from __future__ import annotations
from data_structures import ArraySortedList, LinkedList
from data_structures.array_set import ArraySet
from data_structures.referential_array import ArrayR
from data_structures.array_list import ArrayList
from enums import TeamGameResult
from game_simulator import GameSimulator, GameSimulationOutcome
from dataclasses import dataclass
from team import Team


@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html

    Do not make any changes to this class.
    """
    home_team: Team = None
    away_team: Team = None


class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game] | ArrayList[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        
        No complexity analysis is required for this function.
        Do not make any changes to this function.
        """
        self.games = games
        self.week: int = week

    def __iter__(self):
        """
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            The best and worst complexity of this method are both O(1) as it only involve assigning variable to a value and returning statement which are all constant time operations.
        """
        self.current_index = 0
        return self

    def __next__(self):
        """
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            Best case and worst complexity for this method are both O(1) because in every call it only checks a simple condition, accesses one element from
            self.games by index, increments self.current_index by 1, and returns the game — all of which are constant-time operations, independent of the number of games.
        """
        if self.current_index >= len(self.games):
            raise StopIteration

        current_game = self.games[self.current_index]
        self.current_index +=1
        return current_game


class Season:

    def __init__(self, teams: ArrayR[Team] | ArrayList[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams played in this season.

        Complexity:
            n= number of teams in the season

            Best Case Complexity: O(n^2)
            Worst Case Complexity: O(n^2)

            Assigning teams to self.teams is a constant-time operation. ArraySortedList initialization is O(n) where n is the number of teams, as it allocates space for n elements.
            Best case of add()  is when ArraySortedList is not full and the team is needed to add at the last position in the leaderboard by binary search, and shuffling right is not required,
            ie. O(log n) + O(1) = O(log n) in add().
            Worst case of add() is when ArraySortedList is full, resizing is required and the team is needed to add at the first position in the list by binary search, and shuffling right is required,
            ie. O(n) + O(log n) + O(n) = O(n) in add(),
            The first for loop iterate for n times thus the overall complexity for adding all the teams into the leaderboard initially is O(n) * O(log n) = O(n log n) for best case or O(n) * O(n) = O(n^2) for worst case.
            Creating an empty LinkedList is a constant-time operation. The _generate_schedule() method has a complexity of O(n^2).
            The second for loop iterate based on how many weekly games are there in this season which is calculated by: n(n-1) / (n/2)  = 2(n-1), which simplifies to a complexity of O(n).
            Each append operation in LinkedList is O(1), since it maintains a tail pointer.
            Thus, the overall complexity of __init__() are the same because when best case of add() happens, the complexity is O(1) + O(n) + O(n log n) + O(1) + O(n^2) + O(n) = O(n^2)
            or when worst case of add() happens, the complexity is O(1) + O(n) + O(n^2) + O(1) + O(n^2) + O(n) = O(n^2) too.
        """
        self.teams = teams

        self.leaderboard = ArraySortedList(len(self.teams))

        # adding all the teams into the leaderboard initially
        for team in self.teams:
            self.leaderboard.add(team)

        # generating the schedule
        self.schedule = LinkedList()
        generated_schedule = self._generate_schedule()
        week = 1

        # setting up the schedule by appending all the weeks of the games into linkedlist
        for weekly_games in generated_schedule:
            self.schedule.append(WeekOfGames(week, weekly_games))
            week += 1

    def _generate_schedule(self) -> ArrayList[ArrayList[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:
            ArrayList[ArrayList[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        
        Do not make any changes to this function.
        """
        num_teams: int = len(self.teams)
        weekly_games: ArrayList[ArrayList[Game]] = ArrayList()
        flipped_weeks: ArrayList[ArrayList[Game]] = ArrayList()
        games: ArrayList[Game] = ArrayList()

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: ArrayList[Game] = ArrayList()
            flipped_week: ArrayList[Game] = ArrayList()
            used_teams: ArraySet = ArraySet(len(self.teams))

            week_game_no: int = 0
            for game in games:
                if game.home_team.name not in used_teams and game.away_team.name not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.name)
                    used_teams.add(game.away_team.name)

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(current_week)
            flipped_weeks.append(flipped_week)
            week += 1

        for flipped_week in flipped_weeks:
            weekly_games.append(flipped_week)

        return weekly_games


    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
            Remember to define your variables in your complexity.

            t= number of teams in the season
            k= length of the key
            n= the number of items (key-value tuples) in all the linked list across all hash position of the hash table
            m= the number of players in the linked list(value) of a player position (key)
            p= the number of player positions
            g= total goalscorers

            The outer loop iterates based on how many weekly games are there in this season which is calculated by: t(t-1) / t/2  = 2(t-1), which simplifies to a complexity of O(t).
            The inner loop iterates based on how many games are there in a week which is calculated by: t/2, which simplifies to a complexity of O(t) too.
            For the best case of stimulate_season() method, removing both teams from the leaderboard takes O(1) operation as the best case of remove() method is O(1) when the team is removed behind where shuffling left is not required.
            For the worst case of stimulate_season() method, removing both teams from the leaderboard takes O(n) operation as the worst case of remove() method is O(n) when the team is removed in front where shuffling left is required.
            Assume GameSimulator.simulate() is O(1)
            Updating team results require constant time operation as add_result() method has a complexity of O(1).
            To update a player's goal, it requires g iterations to loop through all the goalscorers which has a complexity of O(g). To find which player scored a goal, it is required to iterate through all
            the players in the team by invoking get_players() method, which has complexity of O(p * n * k + p * m).

            Best Case Complexity: O(t^2 * log t)
            The best case is when all the goalscorers are from home team and does not need to enter the else case. Thus, the overall complexity for this for loop is O(g) * O(p * n * k + p * m).
            Updating the leaderboard has a best complexity of O(log t) when the team is added at the end of the leaderboard where shuffling left is not required.
            Thus, the overall best complexity is O(t) * O(t) * ( O(1) + O(1) + O(1) + ( O(g) * O(p * n * k + p * m) ) + O(log t) )
            =( O(t^2) * O( g * p * n * k + g * p * m) ) + O(t^2 * log t)
            = O(t^2 * log t)

            Worst Case Complexity: O(t^3)
            The worst case is when all the goalscorers are from away team, thus after iterating all the players in home team, it will enter the else case which iterates all the player from away team.
            Thus, the overall complexity for this loop is O(g) * ( O(p * n * k + p * m) + O(p * n * k + p * m) ) = O(g) * O(p * n * k + p * m).
            Updating the leaderboard has a worst complexity of O(t) when the team is added at the front of the leaderboard where shuffling right is required.
            Thus, the overall worst complexity is O(t) * O(t) * ( O(1) + O(1) + O(1) + ( O(g) * O(p * n * k + p * m) ) + O(t) )
            = ( O(t^2) * O( g * p * n * k + g * p * m) ) + O(t^2 * t)
            = O(t^3)
        """
        for weekly_games in self.schedule:
            for game in weekly_games: #using iter and next here
                home_team = game.home_team
                away_team = game.away_team

                # remove both teams from leaderboard first as their scores will be updated
                self.leaderboard.remove(home_team)
                self.leaderboard.remove(away_team)

                outcome = GameSimulator.simulate(home_team, away_team) #O(1)

                # updating team results:
                # when home team wins
                if outcome.home_goals > outcome.away_goals:
                    home_team.add_result(TeamGameResult.WIN)
                    away_team.add_result(TeamGameResult.LOSS)

                #when away team wins
                elif outcome.home_goals < outcome.away_goals:
                    home_team.add_result(TeamGameResult.LOSS)
                    away_team.add_result(TeamGameResult.WIN)

                # when it is a draw
                else:
                    home_team.add_result(TeamGameResult.DRAW)
                    away_team.add_result(TeamGameResult.DRAW)

                # updating player stats, player goals
                for scorer_name in outcome.goal_scorers:
                    for player in home_team.get_players():
                        if player.name == scorer_name:
                            player.goals+=1
                            break #exit the inner loop of finding players in home team

                    # since goal_scorers is a list of scorers from both teams, if a scorers is not found from the home team
                    # then only it will enter the loop of else case of finding scorers in away team
                    else:
                        for player in away_team.get_players():
                            if player.name == scorer_name:
                                player.goals+=1
                                break

                #updating leaderboard
                self.leaderboard.add(home_team)
                self.leaderboard.add(away_team)

    def delay_week_of_games(self, orig_week: int, new_week: int | None = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (int or None): The new week to move the games to. If this is None, it moves the games to the end of the season.

        Complexity:
            n= number of weeks in the schedule

            Best Case Complexity: O(1)
            Accessing the week (week_to_move = self.schedule[orig_index]) uses __getitem__ which calls __get_node_at_index.
            Best case is when the week about to be delayed is at the first node, thus O(1), which cause deleting the week by delete_at_index() method be O(1) too
            as it just needs to update the head pointer. Best case happens when the week is delayed at the end of the season where it enters the if case as append()
            requires a time complexity of O(1) only. Thus, the overall complexity is O(1) as it only involves constant time operations.

            Worst Case Complexity: O(n)
            Accessing the week (week_to_move = self.schedule[orig_index]) uses __getitem__ which calls __get_node_at_index.
            Worst case is when the week about to be delayed is at the second last node, thus O(n), which cause deleting the week by delete_at_index() method be O(n) too
            as it requires to traverse until the second last nodes/ weeks. Thus, the overall complexity is O(n).
        """
        #delete the week about to be delayed
        ori_index = orig_week - 1 # -1 because index starts from 0
        week_to_move = self.schedule[ori_index]
        self.schedule.delete_at_index(ori_index)

        if new_week is None:
            self.schedule.append(week_to_move)
        else:
            new_index = new_week - 1
            self.schedule.insert(new_index, week_to_move)

    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            Both the best and worst complexity are the same as accessing len requires constant time operation only.
        """
        return len(self.teams)

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the season object.

        Complexity:
            Analysis not required.
        """
        return f"Season(Number of teams this = {len(self.teams)}, Number of game weeks this season = {len(self.schedule)})"

    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return str(self)

