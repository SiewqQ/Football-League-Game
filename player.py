from __future__ import annotations
from enums import PlayerPosition
from lazy_double_table import LazyDoubleTable
# Do not change the import statement below
# If you need more modules and classes from datetime, do not use
# separate import statements. Use them from datetime like this:
# datetime.datetime, or datetime.date, etc.
import datetime


class Player:

    def __init__(self, name: str, position: PlayerPosition, age: int) -> None:
        """
        Constructor for the Player class

        Args:
            name (str): The name of the player
            position (PlayerPosition): The position of the player
            age (int): The age of the player

        Complexity:
            n= the table size

            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)

            The best and worst case complexity are the same as the complexity of initializing player class are all O(1) except for the creation of LazyDoubleTable,
            as allocating memory of size n has a complexity of O(n), which dominates other complexity.
        """
        self.name = name
        self.position = position
        self.birth_year = datetime.date.today().year - age #getting the birth year although age is entered
        self.goals = 0
        self.stats = LazyDoubleTable() # a dict/ hash table

    def reset_stats(self) -> None:
        """
        Reset the stats of the player.
        
        This doesn't delete the existing stats, but resets them to 0.
        I.e. all stats that were previously set should still be available, with a value of 0.

        Complexity:
            k = number of keys in the table
            n = the table size

            Best Case Complexity: O(k * len(key))
            The for loop will iterate k times, Thus, O(k).
            Updating the value of the statistic key will invoke __setitem__() magic method which invoke the __hashy_probe() method too.
            The best case of __hashy_probe() method when is_insert = True is O(len(key)). Best case in __hashy_probe() method is when adding a new key,
            an empty position is found exactly at the hash position of the key where no collision occurs, which is at the first iteration of the for loop.
            Since the for loop in reset_stats() method iterate k times, the overall complexity of reset_stats() method is
            O(k) * O(len(key)) = O(k * len(key))

            Worst Case Complexity: O(k * len(key) + k * n * comp (str))
            The for loop will iterate k times, Thus, O(k).
            Updating the value of the statistic key will invoke __setitem__() magic method which invoke the __hashy_probe() method too.
            The worst case of __hashy_probe() method when is_insert = True is O(len(key) + n * comp(str)).
            Worst case in __hashy_probe() method is when adding a new key, all the reachable slots by stepping already have an item,
            except when an empty position/DeletedItemObject is found at the last iteration of iterating table size, this cause the for loop to loop through the items in hash table due to collisions.
            Since the for loop in reset_stats() method iterate k times, the overall complexity of reset_stats() method is
            O(k) * O(len(key) + n * comp(str)) = O(k * len(key) + k * n * comp (str))
        """
        #looping through the keys
        for stat in self.stats.keys(): #O(n)
            self.stats[stat] = 0 # best: O(len(key)), worst: O(n * len(key) + n^2 * comp(str)), n=table size )

    def __setitem__(self, statistic: str, value: int) -> None:
        """
        Set the given value for the given statistic for the player.

        Args:
            statistic (string): The key of the stat
            value (int): The value of the stat

        Complexity:
            n = the table size

            Best Case Complexity: O(len(key))
            While setting a value in the hash table, the position of the statistic key is found by invoking __hashy_probe() method, the best case of __hashy_probe() method when is_insert = True
            is O(len(key)). Best case in __hashy_probe() method is when adding a new key, an empty position is found exactly at the hash position of the key where no collision occurs,
            which is at the first iteration of the for loop. Thus, the overall complexity is dominated by the best case __hashy_probe() complexity.

            Worst Case Complexity: O(n * len(key) + n^2 * comp(str))
            While setting a value in the hash table, the position of the statistic key is found by invoking __hashy_probe() method, the worst case of __hashy_probe() method when is_insert = True
            is O(len(key) + n * comp(str)). Worst case in __hashy_probe() method is when adding a new key, all the reachable slots by stepping already have an item,
            except when an empty position/DeletedItemObject is found at the last iteration of iterating table size, this cause the for loop to loop through the items in hash table due to collisions.
            Worst case of __setitem__() method happens when the hash table requires rehashing after adding an item, the worst case of __rehash() method is O(n * len(key) + n^2 * comp(str)).
            Thus, the overall complexity is dominated by the __rehash() complexity, ie. (O(len(key) + n * comp(str))) + (O(n * len(key) + n^2 * comp(str))) = O(n * len(key) + n^2 * comp(str))
        """
        self.stats[statistic] = value

    def __getitem__(self, statistic: str) -> int:
        """
        Get the value of the player's stat based on the passed key.

        Args:
            statistic (str): The key of the stat

        Returns:
            int: The value of the stat

        Complexity:
            n = the table size

            Best Case Complexity: O(len(key))
            When __getitem__() is invoked, the position of the statistic key is found by invoking __hashy_probe() method, the best case of __hashy_probe() method when is_insert = False
            is O(len(key)). Best case in __hashy_probe() method is when searching for an existing key, the tuple storing the wanted key and value is found exactly at the hash position of the key without probing,
            Thus, the overall complexity of __getitem__() is dominated by the best case of __hashy_probe() complexity

            Worst Case Complexity: O(len(key) + n * comp(str))
            When __getitem__() is invoked, the position of the statistic key is found by invoking __hashy_probe() method, the worst case of __hashy_probe() method when is_insert = False
            is O(len(key) + n * comp(str)). Worst case in __hashy_probe() method is when all the reachable slots by stepping do not have the key we are searching for until we reach the last iteration of iterating the table size.
            Thus, the overall complexity of __getitem__() is dominated by the worst case of __hashy_probe() complexity
        """
        return self.stats[statistic]

    def get_age(self) -> int:
        """
        Get the age of the player

        Returns:
            int: The age of the player

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            The best and worst case complexity are the same because every operation inside get_age() method ie. getting the current year now,
            and subtracting self.birth_year takes constant time, independent of any input size. Thus, O(1).
        """
        return datetime.datetime.now().year - self.birth_year

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the player object.

        Complexity Analysis not required.
        """
        stats_str = ", ".join(f"{key}: {self.stats[key]}" for key in self.stats.keys())
        return (
            f"Player: {self.name}\n"
            f"Position: {self.position.name}\n"  # Assuming PlayerPosition is an enum
            f"Age: {self.get_age()}\n"
            f"Goals: {self.goals}\n"
            f"Stats: {{{stats_str}}}"
        )

    def __repr__(self) -> str:
        """ String representation of the Player object.
        Useful for debugging or when the Player is held in another data structure.
        """
        return str(self)
