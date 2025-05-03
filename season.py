from __future__ import annotations
from data_structures import ArraySortedList, LinkedList
from data_structures.array_set import ArraySet
from data_structures.referential_array import ArrayR
from data_structures.array_list import ArrayList
from enums import TeamGameResult, PlayerPosition
from game_simulator import GameSimulator, GameSimulationOutcome
from dataclasses import dataclass

from player import Player
from random_gen import RandomGen
from team import Team
from tests.helper import take_out_from_adt


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

            Assigning teams to self.teams is a constant-time operation. ArraySortedList initialization is O(N) where N is the number of teams, as it allocates space for N elements.
            Best case of add()  is when ArraySortedList is not full and the team is needed to add at the last position in the leaderboard by binary search, and shuffling right is not required,
            ie. O(log n) + O(1) = O(log n) in add().
            Worst case of add() is when ArraySortedList is full, resizing is required and the team is needed to add at the first position in the list by binary search, and shuffling right is required,
            ie. O(n) + O(log n) + O(n) = O(n) in add(),
            The loop iterate for n times thus the overall complexity for adding all the teams into the leaderboard initially is O(n) * O(log n) or O(n) * O(n)
            Creating an empty LinkedList is a constant-time operation. The _generate_schedule() method has a complexity of O(n^2).
            The loop iterate based on how many weekly games are there in this season which is calculated by: n(n-1) / n/2  = 2(n-1), which simplifies to a complexity of O(n).
            Each append operation in LinkedList is O(1), since it maintains a tail pointer.
            Thus, the overall complexity of __init__() are the same because when best case of add() happens, the complexity is O(1) + O(n) + O(n log n) + O(1) + O(n^2) + O(n) = O(n^2)
            or when worst case of add() happens, the complexity is O(1) + O(n) + O(n^2) + O(1) + O(n^2) + O(n) = O(n^2) too.
        """
        self.teams = teams

        self.leaderboard = ArraySortedList(len(self.teams)) #O(n)

        # adding all the teams into the leaderboard initially
        for team in self.teams: #O(n)n
            self.leaderboard.add(team) # best: O(log n), worst: O(n)

        self.schedule = LinkedList() # O(1)

        generated_schedule = self._generate_schedule() #O(n^2)
        week = 1 # O(1)
        #setting up the schedule by appending all the weeks of the games into linkedlist
        for weekly_games in generated_schedule: #O(g), which is O(n) too because number of weekly games = n(n-1) / n/2  = 2(n-1)
            self.schedule.append(WeekOfGames(week, weekly_games)) #O(1)
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
            k= size of key
            n= the number of items (key value tuples) in the linked list at a hash position, ie. table size of HashTableSeparateChaining
            m= the number of items (players) in the linked list(value) of a player position (key)
            p= the number of player positions

            The outer loop iterates based on how many weekly games are there in this season which is calculated by: t(t-1) / t/2  = 2(t-1), which simplifies to a complexity of O(t).
            The inner loop iterates based on how many games are there in a week which is calculated by: t/2, which simplifies to a complexity of O(t) too.
            Removing both teams from the leader takes O(1) operation as the best case of remove() method is O(1) when the team is removed behind where shuffling left is not required.
            Assume GameSimulator.simulate() is O(1)
            Updating team results require constant time operation as add_result() method has a complexity of O(1).
            To update a player's goal, it requires g iterations to loop through all the goalscorers which has a complexity of O(g), to find which player scored a goal, it is required to iterate through all
            the players in the team by invoking get_players() method, which has complexity of O(p * (k + n * comp(str) + m)).

            Best Case Complexity: O(t^2 * log t)
            The best case is when all the goalscorers are from home team and does not need to enter the else case. Thus, the overall complexity for this for loop is O(g) * O(p * (k + n * comp(str) + m).
            Updating the leaderboard has a best complexity of O(log t) when the team is added at the end of the leaderboard where shuffling left is not required.
            Thus, the overall best complexity is O(t) * ( O(t) * ( O(1) + O(1) + O(1) + (O(g) * O(p * (k + n * comp(str) + m)) + O(log t)) ) )
            = O(t^2 * g * p * (k + n * comp(str) + m)) + O(t^2 * log t)
            = O(t^2 * log t)

            Worst Case Complexity: O(t^3)
            The worst case is when all the goalscorers are from away team, thus after iterating all the players in home team, it will enter the else case which iterates all the player from away team.
            Thus, the overall complexity for this loop is O(g) * (O(p * (k + n * comp(str) + m) + O(p * (k + n * comp(str) + m)) = O(g) * O(p * (k + n * comp(str) + m).
            Updating the leaderboard has a worst complexity of O(t) when the team is added at the front of the leaderboard where shuffling right is required.
            Thus, the overall worst complexity is O(t) * ( O(t) * ( O(1) + O(1) + O(1) + (O(g) * O(p * (k + n * comp(str) + m)) + O(t) ) )
            = O(t^2 * g * p * (k + n * comp(str) + m)) + O(t^2 * t)
            = O(t^3)
        """

        for weekly_games in self.schedule: #O(t), n= number of teams in the season
            for game in weekly_games: #using iter and next here  #O(t) too, since games in a week= t/2

                # remove both teams from leaderboard first as their scores will be updated
                self.leaderboard.remove(game.home_team) #best: O(1) delete behind, worst: O(t) delete at front, shift left
                self.leaderboard.remove(game.away_team) #best: O(1) delete behind, worst: O(t) delete at front, shift left

                outcome = GameSimulator.simulate(game.home_team, game.away_team) #O(1)

                # updating team results:
                # when home team wins
                if outcome.home_goals > outcome.away_goals:
                    game.home_team.add_result(TeamGameResult.WIN) #O(1)
                    game.away_team.add_result(TeamGameResult.LOSS) #O(1)

                #when away team wins
                elif outcome.home_goals < outcome.away_goals:
                    game.home_team.add_result(TeamGameResult.LOSS)
                    # print(TeamGameResult.LOSS)
                    game.away_team.add_result(TeamGameResult.WIN)

                # when it is a draw
                else:
                    game.home_team.add_result(TeamGameResult.DRAW)
                    game.away_team.add_result(TeamGameResult.DRAW)
                    # print(game.away_team.get_history())

                # updating player stats, player goals
                for scorer_name in outcome.goal_scorers: #O(g), g= total goal scorers
                    for player in game.home_team.get_players(): #getting all the players in home_team  #worst: O(p * (k + n * comp(str) + m))
                        # k= size of key, m= the number of items (players) in the linked list(value) of a player position (key), n= the number of items (key value tuples) in the linked list at a hash position, ie. table size of HashTableSeparateChaining
                        if player.name == scorer_name: #O(comp(str))?
                            player.goals+=1 #O(1)
                            break #exit the inner loop of finding players in home team

                    # since goal_scorers is a list of scorers from both teams, if a scorers is not found from the home team
                    # then only it will enter the loop of finding scorers in away team
                    else:
                        for player in game.away_team.get_players(): #worst: O(p * (k + n * comp(str) + m))
                            if player.name == scorer_name: #O(comp(str))?
                                player.goals+=1 #O(1)
                                break

                #updating leaderboard
                self.leaderboard.add(game.home_team)
                self.leaderboard.add(game.away_team)
                #Best case: item position is last, no need shuffle teams to right: O(log t) + O(1) = O(log t)
                # Worst case: item position is first, shuffle all teams to right: O(log t) + O(t) = O(t)
                print(game.home_team.get_history())

        # print("SEASON COMPLETE FINAL LEADERBOARD:")
        # leaderboard_list = [team for team in self.leaderboard]  # Convert to list
        # for i, team in enumerate(leaderboard_list, 1):
        #     print(f"{i}. {team.name} (Points: {team.points})")

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
            Best case is when the week about to be delayed is at the first node, thus O(1), which cause deleting the week by delete_at_index() method
            be O(1) too as it just needs to update the head pointer. Best case happens when the week is delayed at the end of the season where append()
            requires a time complexity of O(1) only. Thus, the overall complexity is O(1) as it only involves constant time operations.

            Worst Case Complexity: O(n)
            Accessing the week (week_to_move = self.schedule[orig_index]) uses __getitem__ which calls __get_node_at_index.
            Worst case is when the week about to be delayed is at the last node, thus O(n), which cause deleting the week by delete_at_index() method
            be O(n) too as it requires to traverse the entire nodes/ weeks. Worst case happen when the week is inserted near the end of the season where insert()
            requires a time complexity of O(n) too. Thus, the overall complexity is O(n).
        """
        #delete the week about to be delayed
        orig_index = orig_week - 1
        week_to_move = self.schedule[orig_index]
        self.schedule.delete_at_index(orig_index) #O(1) best, worst O(n)

        if new_week is None:
            self.schedule.append(week_to_move) #O(1)
        else:
            new_index = new_week - 1
            self.schedule.insert(new_index, week_to_move) #O(1) best, worst O(n)


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

if __name__ == '__main__':
    def setUp() -> None:
        RandomGen.set_seed(123)

        first_names = [
            "John", "Jane", "Alice", "Bob", "Charlie", "David",
            "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy",
            "Mallory", "Niaj", "Olivia", "Peggy", "Robert", "Sybil",
            "Trent", "Uma", "Victor", "Walter", "Xena", "Yara", "Zane"
        ]
        last_names = [
            "Smith", "Johnson", "Williams", "Jones", "Brown",
            "Davis", "Miller", "Wilson", "Moore", "Taylor",
            "Anderson", "Thomas", "Jackson", "White", "Harris",
            "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
        ]
        team_names = [
            "Tornadoes", "Sharks", "Wolves", "Eagles", "Lions", "Dragons",
            "Panthers", "Bears", "Hawks", "Falcons", "Tigers", "Mustangs",
        ]

        # Create random teams
        NUMBER_OF_TEAMS = 6
        NUMBER_OF_PLAYERS_PER_POSITION = 4

        teams: list[Team] = []
        used_names = set()
        for i in range(NUMBER_OF_TEAMS):
            players = []
            for pos in PlayerPosition:
                for _ in range(NUMBER_OF_PLAYERS_PER_POSITION):
                    player_name = f"{RandomGen.random_choice(first_names)} {RandomGen.random_choice(last_names)}"
                    while player_name in used_names:
                        player_name = f"{RandomGen.random_choice(first_names)} {RandomGen.random_choice(last_names)}"
                    used_names.add(player_name)
                    player = Player(player_name, pos, RandomGen.randint(18, 40))
                    players.append(player)
            team = Team(team_names[i], ArrayR.from_list(players), RandomGen.randint(5, 15))
            teams.append(team)

        season = Season(ArrayR.from_list(teams))
        season.simulate_season()  # This is what triggers the printing!
        print(season)
    setUp()
