from __future__ import annotations
from data_structures import ArrayList, CircularQueue
from data_structures.linked_list import LinkedList
from data_structures import HashTableSeparateChaining
from data_structures.referential_array import ArrayR
from enums import TeamGameResult, PlayerPosition
from player import Player
from hashy_date_table import HashyDateTable
from typing import Collection, TypeVar

T = TypeVar("T")


class Team:
    def __init__(self, team_name: str, initial_players: ArrayR[Player], history_length: int) -> None: #complexity same as lazy double
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
            d = the table size of HashyDateTable
            p = the number of player positions
            m = the number of initial players
            k = size of key
            n= the number of items (key value tuples) in the linked list at a hash position

            Best Case Complexity: O(h + d + (k * (p + m)))
            Instantiating a CircularQueue of size h requires a complexity of O(h) while instantiating a HashyDateTable of size d has a complexity of O(d).
            Instantiating a HashTableSeparateChaining of size p requires a complexity of O(p)
            While inserting all the player positions into the hash table, __setitem__ magic method is invoked which has a best case of O(k) when
            there is no linked list at the hash position. After assigning a new linked list at the hash position, the item(tuple) ie. the position name as key and linked list as data in the tuple
            is inserted at the head of the new linked list at the hash position. Therefore, the overall complexity of this first for loop is O(p * k).
            While adding initial players to the value part of tuple which is the linked list of a key, the add_player() method is used.
            The best case happens when the wanted item(tuple) is found at the first iteration, after comparing the key (str) with tuple key, which has a best complexity of O(m * (k+comp(str))),
            the player is then appended to the value part of linked list in the tuple.
            Therefore, the overall best complexity is: O(h) + O(d) + O(p) + O(p * k) + O(m * k) = O(h + d + (k * (p + m)))

            Worst Case Complexity:( h + d + ( (p + m) * (k + (n * comp(str))) ) )
            Instantiating a CircularQueue of size h requires a complexity of O(h) while instantiating a HashyDateTable of size d has a complexity of O(d).
            Instantiating a HashTableSeparateChaining of size p requires a complexity of O(p)
            While inserting all the player positions into the hash table, __setitem__ magic method is invoked which has a worst case of O(k + n * comp(str)) when
            there is ald a linked list containing items (tuple) at the hash position (collision), and the wanted item (tuple) is found at the last iteration of the hash position linked list,
            after comparing the key str to the tuple key / or the tuple is not found, ie. adding a new item (tuple), where the key is position name and value is linked list, at the tail of
            linked list at the hash position. Therefore, the overall complexity of this first for loop is O(p * (k + n * comp(str))).
            While adding initial players to the value part of tuple which is the linked list of a key, the add_player() method is used.
            The worst case happens when the wanted item(tuple) is found at the last iteration, after comparing the key (str) with tuple key, which has a worst complexity of O(m * (k + n * comp(str))),
            the player is then appended to the value part of linked list in the tuple.
            Therefore, the overall worst complexity is: O(h) + O(d) + O(p) + O(p * (k + n * comp(str))) + O(m * (k + n * comp(str))) = O( h + d + ( (p + m) * (k + (n * comp(str))) ) )
        """
        self.name = team_name
        self.points = 0

        self.history_length = history_length
        self.results_history = CircularQueue(self.history_length) # O(h), h = history length

        self.posts = HashyDateTable() #O(d), d= table size of hashy date

        self.players = HashTableSeparateChaining(len(PlayerPosition)) # O(p), p = number of player position

        # inserting position name as the key and linkedlist as the value
        for position in PlayerPosition: #O(p)
            self.players[position.name]=LinkedList() #setitem: best: O(k), worst: O(k + n * comp(str)), k = length of key, n = number of item in the key

        # Adding initial players to value part of hash table which is a linked list
        for player in initial_players: #O(m), m = number of players
          self.add_player(player) #Best: O(k + comp(str)), worst: O(k + n * comp(str))


    def add_player(self, player: Player) -> None:   #complexity same as lazy double
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            k= size of key
            n= the number of items (key value tuples) in the linked list at a hash position,  ie. table size of HashTableSeparateChaining

            Best Case Complexity: O(k)
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a best complexity of O(k + comp(str)) = O(k)
            when the wanted item(key value tuple) is found at the first iteration of iterating the number of items(key value tuple) in the hash table, after comparing the key (str) with tuple key.
            Appending the player has a complexity of O(1) as there is a reference to the rear of linked list.
            The overall complexity of this method is dominated by the __getitem__ magic method.

            Worst Case Complexity: O(k + n * comp(str))
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a worst complexity of O(k + n * comp(str))
            when the wanted item(key value tuple) is found at the last iteration of iterating the number of items(key value tuple) in the hash table, after comparing the key (str) with tuple key at each iteration.
            Appending the player has a complexity of O(1) as there is a reference to the rear of linked list.
            The overall complexity of this method is dominated by the __getitem__ magic method.
        """
        # finding the position of player
        position_name = player.position.name

        # adding the player to linked list in hash table according to the position key
        player_linked_list = self.players[position_name] #getitem, Best: O(k + comp(str)), worst: O(k + n * comp(str))
        player_linked_list.append(player)  #O(1), own self append to linked list in hash, not by using hash method , so see linked list complexity here

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            k= size of key
            n= the number of items (key value tuples) in the linked list at a hash position,  ie. table size of HashTableSeparateChaining
            m= the number of items (players) in the linked list(value) of a player position (key)

            Best Case Complexity: O(k)
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a best complexity of O(k + comp(str)) = O(k),
            when the wanted item(key value tuple) is found at the first iteration of iterating the number of items(key value tuple) in the hash table, after comparing the key (str) with tuple key.
            Best case happens when the player we are trying to delete from the linked list(value) of a player position(key) is at the head of the linked list where it does not need to traverse the nodes. Thus, O(1).
            Therefore, the overall best complexity of this method is O(k) + O(1) = O(k)

            Worst Case Complexity: O(k + n * comp(str) + m)
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a worst complexity of O(k + n * comp(str))
            when the wanted item(key value tuple) is found at the last iteration of iterating the number of items(key value tuple) in the hash table, after comparing the key (str) with tuple key at each iteration.
            Worst case happens when the player we are trying to delete from the linked list(value) of a player position(key) is at the tail of the linked list where it is required to traverse the entire nodes. Thus, O(n).
            Therefore, the overall worst complexity of this method is O(k + n * comp(str)) + O(m) = O(k + n * comp(str) + m)
        """
        position_name = player.position.name
        player_linked_list=self.players[position_name] #getitem, Best: O(k + comp(str)), worst: O(k + n * comp(str))

        try:
            player_linked_list.remove(player) # best case: item to delete is at the head of the list, O(1), worst case: item to delete is at the tail of the list, O(m)
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
            k= size of key
            n= the number of items (key value tuples) in the linked list at a hash position, ie. table size of HashTableSeparateChaining
            m= the number of items (players) in the linked list(value) of a player position (key)
            p= the number of player positions

            Best Case Complexity: O(k + m)
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a best complexity of O(k + comp(str)) = O(k),
            when the wanted item(key value tuple) is found at the first iteration of iterating the number of items(key value tuple) in the hash table, after comparing the key (str) with tuple key.
            Best case happens when a position name is inputted, thus it enters the if statement. Looping every player in the linked list(value) of a player position (key) requires a time complexity of O(m),
            where every player is appended to the new linked list created which has a time complexity of O(1). Thus the overall complexity of this 'if' case 'for' loop is O(m).
            The overall best case complexity for this method is O(k) + O(m) = O(k + m)

            Worst Case Complexity: O(p * (k + n * comp(str) + m))
            Worst case happens when the position name is none, thus it enters the else statement. Looping every player position that exist has a time complexity of O(p).
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a worst complexity of O(k + n * comp(str))
            when the wanted item(key value tuple) is found at the last iteration of iterating the number of items(key value tuple) in the hash table, after comparing the key (str) with tuple key at each iteration.
            Looping every player in the linked list(value) of a player position (key) requires a time complexity of O(m), where every player is appended to the new linked list created which has a time complexity of O(1).
            Thus, the overall worst case complexity for this method is O(p) * (O(k + n * comp(str)) + O(m * 1)) = O(p * (k + n * comp(str) + m))
        """
        collection = LinkedList()

        # if we are given a position
        if position is not None:
            # for every player in the given position, add it to collection
            for player in self.players[position.name]: # getitem, Best: O(k + comp(str)), worst: O(k + n * comp(str)), #looping the linked list, O(m), number of players in player linked list
                collection.append(player) #O(1)
                print(player)
        else:
            for position in PlayerPosition: #O(p)
                for player in self.players[position.name]: # getitem, Best: O(k + comp(str)), worst: O(k + n * comp(str)), #looping the linked list, O(m), number of players in player linked list
                    collection.append(player) #O(1)

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
            n= the number of items (key value tuples) in the linked list at a hash position, ie. the table size of HashyDateTable

            Best Case Complexity: O(1)
            While inserting a key-value pair, the __setitem__() magic method of LinearProbeTable is invoked as HashyDateTable is inherited from LinearProbeTable.
            The best case complexity of __linear_probe() method is O(hash(key)), which is the complexity of the hash function, when first position is empty. Since HashyDateTable
            is the child class of LinearProbeTable, thus the hash() method of HashDateTable overwrites the hash() method in LinearProbeTable, which has a complexity of O(1).
            Thus, the overall best complexity of this method is O(1).

            Worst Case Complexity: O(n)
            While inserting a key-value pair, the __setitem__() magic method of LinearProbeTable is invoked as HashyDateTable is inherited from LinearProbeTable.
            The worst case complexity of __linear_probe() method is O(hash(key) + n * comp(str)), when we've searched the entire table to find the key. Since HashyDateTable
            is the child class of LinearProbeTable, thus the hash() method of HashDateTable overwrites the hash() method in LinearProbeTable, which has a complexity of O(1).
            The input of HashyDateTable will always be a date with fixed length of 10, thus the complexity of comparing of str can be simplified to O(1).
            Thus, the overall best complexity of this method is O(1 + n * 1) = O(n)
        """

        self.posts[post_date] = post_content

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
            p= the number of player positions
            k= size of key
            n= the number of items (key value tuples) in the linked list at a hash position, ie. table size of HashTableSeparateChaining

            Best Case Complexity: O(p * k)
            The for loop iterate as many times as how many player position there are. Thus, O(p).
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a best complexity of O(k + comp(str)) = O(k),
            when the wanted item(key value tuple) is found at the first iteration of iterating the number of items(key value tuple) in the hash table, after comparing the key (str) with tuple key.
            Thus, the overall best case complexity is O(p) * O(k).

            Worst Case Complexity: O(p * (k + n * comp(str)))
            The for loop iterate as many times as how many player position there are. Thus, O(p).
            Finding the linked list(value) of a player position(key) will invoke the __getitem__ magic method which has a worst complexity of O(k + n * comp(str))
            when the wanted item(key value tuple) is found at the last iteration of iterating the number of items(key value tuple) in the hash table, after comparing the key (str) with tuple key at each iteration.
            Thus, the overall worst case complexity is O(p) * O(k + n * comp(str)).
        """
        count = 0

        for position in PlayerPosition: #O(p)
            count += len(self.players[position.name]) # getitem, Best: O(k + comp(str)), worst: O(k + n * comp(str))
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
        """Returns True if two teams have the same name and points."""
        if not isinstance(other, Team):
            return False
        return (self.name == other.name) and (self.points == other.points)

    def __gt__(self, other):
        """
        Returns the greater than boolean, ie. a team is greater than another team if the team has fewer points
        Thus, the team that is greater is the team with lesser points and will come later in the Sorted List
        """
        if self.points != other.points:
            return self.points < other.points #more points comes first (descending)

        #if two teams have the same points, sort by name
        return self.name > other.name

    def __ge__(self, other):
        """Returns True if this team has fewer points or same points and a name >= other's name."""
        if self.points != other.points:
            return self.points <= other.points  # More points come first (descending)
        return self.name >= other.name  # Tie-break: name (ascending)

    def __lt__(self, other):
        """
        Returns the less than boolean, ie. a team is lesser than another team if the team has more points
        Thus, the team that is smaller is the team with more points and will come first in the Sorted List
        """
        if self.points != other.points:
            return self.points > other.points # Lower points come later

        #if two teams have the same points, sort by name
        return self.name < other.name

    def __le__(self, other):
        """Returns True if this team has more points or same points and a name <= other's name."""
        if self.points != other.points:
            return self.points >= other.points  # Fewer points come later (descending)
        return self.name <= other.name  # Tie-break: name (ascending)
