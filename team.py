from __future__ import annotations
from data_structures import CircularQueue
from data_structures.linked_list import LinkedList
from data_structures import HashTableSeparateChaining
from data_structures.referential_array import ArrayR
from enums import TeamGameResult, PlayerPosition
from player import Player
from hashy_date_table import HashyDateTable
from typing import Collection, TypeVar

T = TypeVar("T")


class Team:
    def __init__(self, team_name: str, initial_players: ArrayR[Player], history_length: int) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            initial_players (ArrayR[Player]): The players the team starts with initially
            history_length (int): The number of `GameResult`s to store in the history

        Returns:
            None

        Complexity:
            h = the history length
            p = the number of player positions
            m = the number of players
            k = length of the key
            n= the number of items (key-value tuples) in all the linked list across all hash position of the hash table

            Instantiating a CircularQueue of size h requires a complexity of O(h) while instantiating a HashyDateTable has a complexity of O(1) as no size is inputted,
            which lead to a HashyDateTable with constant fixed size of 366 to be created initially. Instantiating a HashTableSeparateChaining of size p requires a complexity of O(p).

            Best Case Complexity: O(h + (k * (p + m)))
            While inserting all the player positions into the hash table, __setitem__ magic method is invoked which has a best case of O(k) when the hashed position is empty without probing, ie.
            no linked list exist yet at the hash position. After assigning a new linked list at the hash position, the item(tuple) ie. the player position name as key and linked list as data in the tuple
            is inserted at the head of the new created linked list at the hash position. Therefore, the overall complexity of this first for loop in __init__() is O(p * k).
            While adding initial players to the value part of tuple which is the linked list of a key, the add_player() method is used.
            The add_player() method will invoke __getitem__() method which has a best case of O(k). The best case happens when the wanted item(tuple) is found at the first iteration, after comparing the key (str) with tuple key,
            the player is then appended to the value part of tuple which is the linked list. Thus, the overall complexity of the second for loop in __init__() is O(m * k).
            Therefore, the overall best complexity is: O(h) + O(1) + O(p) + O(p * k) + O(m * k) = O(h + (k * (p + m)))

            Worst Case Complexity: O(h + ((n * k) * (p + m)))
            While inserting all the player positions into the hash table, __setitem__ magic method is invoked which has a worst case of O(n * k) when
            there is ald a linked list containing items (tuple) at the hash position (collision), and the wanted item (tuple)/ empty position is found
            at the last iteration of iterating the items in the table, ie, at the tail of the linked list at the hash position.
            Therefore, the overall complexity of this first for loop in __init__() is O(p * (n * k)).
            While adding initial players to the value part of tuple which is the linked list of a key, the add_player() method is used.
            The add_player() method will invoke __getitem__() method which has a worst case of O(n * k).
            The worst case happens when the wanted item(tuple) is found at the last iteration of iterating the items in the table.
            the player is then appended to the value part of tuple which is the linked list. Thus, the overall complexity of the second for loop in __init__() is O(m * (n * k)).
            Therefore, the overall worst complexity is: O(h) + O(1) + O(p) + O(p * (n * k)) + O(m * (n * k)) = O(h + ( (p + m) * (n * k) ))
        """
        self.name = team_name
        self.points = 0

        self.history_length = history_length
        self.results_history = CircularQueue(self.history_length)

        self.posts = HashyDateTable()

        self.players = HashTableSeparateChaining(len(PlayerPosition))

        # inserting position name as the key and linkedlist as the value
        for position in PlayerPosition:
            self.players[position.name]=LinkedList()

        # Adding initial players to value part of hash table which is a linked list
        for player in initial_players:
          self.add_player(player)


    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            k= length of the key
            n= the number of items (key-value tuples) in all the linked list across all hash position of the hash table

            Best Case Complexity: O(k)
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a best complexity of O(k)
            when the wanted item(key-value tuple) is found at the first iteration of iterating the number of items(key-value tuple) in the hash table, after comparing the inputted key (str) with tuple key.
            Appending the player has a complexity of O(1) as there is a reference to the rear of linked list.
            The overall complexity of this method is dominated by the __getitem__ magic method, ie. O(k).

            Worst Case Complexity: O(n * k)
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a worst complexity of O(n * k)
            when the wanted item(key-value tuple) is found at the last iteration of iterating the number of items(key-value tuple) in the hash table, after comparing the inputted key (str) with tuple key at each iteration.
            Appending the player has a complexity of O(1) as there is a reference to the rear of linked list.
            The overall complexity of this method is dominated by the __getitem__ magic method, ie. O(n * k).
        """
        # finding the position of player
        position_name = player.position.name

        # adding the player to linked list which is the value part of a player position key
        player_linked_list = self.players[position_name]
        player_linked_list.append(player)

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            k= length of the key
            n= the number of items (key-value tuples) in all the linked list across all hash position of the hash table
            m= the number of players in the linked list(value) of a player position (key)

            Best Case Complexity: O(k)
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a best complexity of O(k),
            when the wanted item(key-value tuple) is found at the first iteration of iterating the number of items(key-value tuple) in the hash table.
            Best case happens when the player we are trying to delete in the linked list(value) of a player position(key)
            is at the head of the linked list where it does not need to traverse the nodes. Thus, O(1).
            Therefore, the overall best complexity of this method is O(k) + O(1) = O(k)

            Worst Case Complexity: O(n * k + m)
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a worst complexity of O(n * k)
            when the wanted item(key-value tuple) is found at the last iteration of iterating the number of items(key-value tuple) in the hash table,
            where the wanted tuple is at the tail of the linked list at the hash position.
            Worst case happens when the player we are trying to delete in the linked list(value) of a player position(key)
            is at the tail of the linked list where it is required to traverse the entire nodes. Thus, O(m).
            Therefore, the overall worst complexity of this method is O(n * k) + O(m) = O(n * k + m)
        """
        position_name = player.position.name
        player_linked_list = self.players[position_name]

        try:
            player_linked_list.remove(player)
        except ValueError:
            raise ValueError(f"Player {player.name} not found in {position_name}")


    def get_players(self, position: PlayerPosition | None = None) -> Collection[Player]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (PlayerPosition or None): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder.

            This includes the ArrayR, which was previously prohibited.

        Complexity:
            k= length of the key
            n= the number of items (key-value tuples) in all the linked list across all hash position of the hash table
            m= the number of players in the linked list(value) of a player position (key)
            p= the number of player positions

            Best Case Complexity: O(k)
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a best complexity of O(k),
            when the wanted item(key-value tuple) is found at the first iteration of iterating the number of items(key value tuple) in the hash table.
            Best case happens when a player position name is inputted, thus it enters the if statement and returns the linked list (value) storing the players of a player position (key).
            The overall best case complexity for this method is O(k).

            Worst Case Complexity: O(p * n * k + p * m)
            Worst case happens when the player position name is none, thus it enters the else statement. Looping through every player position that exist has a time complexity of O(p).
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a worst complexity of O(n * k)
            when the wanted item(key-value tuple) is found at the last iteration of iterating the number of items(key-value tuple) in the hash table, where the wanted tuple is at the tail of the linked list at the hash position
            Looping every player in the linked list(value) of a player position (key) requires a time complexity of O(m), where every player is appended to the new linked list created which has a time complexity of O(1).
            Thus, the overall worst case complexity for this method is O(p) * (O(n * k) + O(m * 1)) = O(p * n * k + p * m)
        """
        collection = LinkedList()

        # if we are given a position
        if position is not None:
            # just return the linked list (value) of the player position name (key)
            return self.players[position.name]

        else:
            for position in PlayerPosition:
                for player in self.players[position.name]:
                    collection.append(player)

        return collection

    def add_result(self, result: TeamGameResult) -> None:
        """
        Add the `result` to this `Team`'s history

        Args:
            result (GameResult): The result to add

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            Both the best and worst case are the same because simple integer addition, is_full() method ie. checking if len(self) == len(self.__array),
            serve() method ie. removing front element by adjusting self.__front and append() method ie. inserting at self.__rear and updates the rear pointer
            are all constant time operations therefore the overall complexity of this method is O(1).
        """
        # Add to points
        self.points += result.value

        # if queue is full, remove the oldest record to ensure latest records are recorded
        if self.results_history.is_full():
            self.results_history.serve()

        self.results_history.append(result)


    def get_history(self) -> Collection[TeamGameResult] | None:
        """
        Returns the `GameResult` history of the team.
        If the team has played less than this team's `history_length`,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the result should be a container with 4 objects in this order:
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        If this method is called before the team has played any games,
        return None the reason for this is explained in the specification.

        Returns:
            Collection[GameResult]: The most recent `GameResult`s for this team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            Both best and worst case are the same because checking the len() of CircularQueue and returning the collection are all constant time operations.
            Therefore, the overall complexity of this method is O(1).
        """
        if len(self.results_history) == 0:
            return None

        return self.results_history

    def make_post(self, post_date: str, post_content: str) -> None:
        """
        Publish a team blog `post` for a particular `post_date`.

        A `Team` can have one published post per day. Any duplicate
        posts should overwrite the original post for that day.

        Args:
            `post_date` (`str`) - The date of the post
            `post_content` (`str`) - The content of the post

        Returns:
            None

        Complexity:
            k= length of the key
            n= the number of items in the table

            Best Case Complexity: O(1)
            While inserting a key-value pair, the __setitem__() magic method of LinearProbeTable is invoked as HashyDateTable is inherited from LinearProbeTable.
            The best case complexity of __linear_probe() method is O(k), which is dominated by the complexity of the hash function, when first position is empty. Since HashyDateTable
            is the child class of LinearProbeTable, thus the hash() method of HashDateTable with complexity of O(1) overwrites the hash() method in LinearProbeTable which was previously O(k).
            Thus, the overall best complexity of this method is O(1).

            Worst Case Complexity: O(n^2 * k)
            While inserting a key-value pair, the __setitem__() magic method of LinearProbeTable is invoked as HashyDateTable is inherited from LinearProbeTable.
            The worst case complexity of __linear_probe() method is O(n * k), which is dominated by the complexity of the hash function.
            Since HashyDateTable is the child class of LinearProbeTable, thus the hash() method of HashDateTable with complexity of O(1) overwrites the hash() method in LinearProbeTable, which was previously O(n * k).
            The hash () method of HashDateTable is O(1) because the input of HashyDateTable will always be a date with fixed length of 10, so the complexity of comparing str can be simplified to O(1).
            Thus, the overall worst complexity of linear probe method is O(1 + n * 1) = O(n)
            Worst case of make_post() method happens when the hash table requires rehashing after adding a new post, the worst case of __rehash() method is O(n^2 * k).
            Thus, the overall complexity is dominated by the __rehash() complexity, ie. O(n) + O(n^2 * k) = O(n^2 * k)
        """
        self.posts[post_date] = post_content

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
            p= the number of player positions
            k= the length of the key
            n= the number of items (key-value tuples) in all the linked list across all hash position of the hash table

            Best Case Complexity: O(p * k)
            The for loop iterate as many times as how many player position there are. Thus, O(p).
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a best complexity of O(k),
            when the wanted item(key value tuple) is found at the first iteration of iterating the number of items(key value tuple) in the hash table.
            Thus, the overall best case complexity is O(p) * O(k).

            Worst Case Complexity: O(p * n * k)
            The for loop iterate as many times as how many player position there are. Thus, O(p).
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a worst complexity of O(n * k)
            when the wanted item(key value tuple) is found at the last iteration of iterating the number of items(key value tuple) in the hash table,
            where the wanted tuple is at the tail of the linked list at the hash position.
            Thus, the overall worst case complexity is O(p) * O(n * k).
        """
        count = 0

        for position in PlayerPosition:
            count += len(self.players[position.name])
        return count

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity analysis not required.
        """
        return f"Team(name={self.name}, points={self.points}, players={len(self)})"

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure.
        """
        return str(self)

    def __eq__(self, other):
        """Returns True if two teams have the same name."""
        if not isinstance(other, Team):
            return False

        return self.name == other.name

    def __gt__(self, other):
        """
        Returns the greater than boolean, ie. a team is greater than another team if the team has fewer points
        Thus, the team that is greater is the team with lesser points and will come later in the Sorted List
        """
        if self.points != other.points:
            return self.points < other.points #more points comes first (descending)

        #if two teams have the same points, sort by name
        return self.name > other.name

    def __lt__(self, other):
        """
        Returns the less than boolean, ie. a team is lesser than another team if the team has more points
        Thus, the team that is smaller is the team with more points and will come first in the Sorted List
        """
        if self.points != other.points:
            return self.points > other.points # lower points come later

        #if two teams have the same points, sort by name
        return self.name < other.name

