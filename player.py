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
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            The best and worst case complexity are the same as the complexity of initializing player class are all O(1) including the creation of LazyDoubleTable,
            as no size is inputted, which lead to a LazyDoubleTable with constant fixed size of 5 to be created initially.
        """
        self.name = name
        self.position = position
        self.birth_year = datetime.date.today().year - age #getting the birth year although age is inputted
        self.goals = 0
        self.stats = LazyDoubleTable()

    def reset_stats(self) -> None:
        """
        Reset the stats of the player.
        
        This doesn't delete the existing stats, but resets them to 0.
        I.e. all stats that were previously set should still be available, with a value of 0.

        Complexity:
            m = the table size
            n = number of items in the table
            k = length of the key

            Best Case Complexity: O(m + n * k)
            Getting all the keys in the hash table by invoking keys() method have a time complexity of O(m). The for loop will iterate n times, Thus, O(n).
            Updating the value of the statistic key will invoke __setitem__() magic method which invoke the __hashy_probe() method too.
            The best case of __hashy_probe() method when is_insert = True is O(k). Best case in __hashy_probe() method is when searching an existing key,
            the key is found exactly at the hash position of the key without probing, where no collision occurs.
            Since the for loop in reset_stats() method iterate n times, the overall complexity of reset_stats() method is O(m) + (O(n) * O(k)) = O(m + n * k)

            Worst Case Complexity: O(m + n^2 * k)
            Getting all the keys in the hash table by invoking keys() method have a time complexity of O(m). The for loop will iterate n times, Thus, O(n).
            Updating the value of the statistic key will invoke __setitem__() magic method which invoke the __hashy_probe() method too.
            The worst case of __setitem__() is not used because while updating the values of existing keys, a rehash will not happen as no new keys are added to the table.
            Thus, The worst case of __hashy_probe() in __setitem__() is used for this method instead. The worst case of __hashy_probe() method when is_insert = True is O(n * k).
            Worst case in __hashy_probe() method is when searching an existing key, all the reachable slots by stepping do not have the key we are searching for,
            except until the last iteration of iterating the items in the table.
            Since the for loop in reset_stats() method iterate n times, the overall complexity of reset_stats() method is O(m) + (O(n) * O(n * k)) = O(m + n^2 * k)
        """
        keys = self.stats.keys()

        for stat in keys:
            self.stats[stat] = 0

    def __setitem__(self, statistic: str, value: int) -> None:
        """
        Set the given value for the given statistic for the player.

        Args:
            statistic (string): The key of the stat
            value (int): The value of the stat

        Complexity:
            n = number of items in the table
            k = length of the key

            Best Case Complexity: O(k)
            While setting a value in the hash table, the __setitem__() magic method of LazyDoubleTable is invoked,
            where the position of the statistic key is found by invoking __hashy_probe() method, the best case of __hashy_probe() method when is_insert = True
            is O(k). Best case in __hashy_probe() method is when adding a new key, an empty position is found exactly at the hash position of the key without probing, where no collision occurs.
            Thus, the overall complexity is dominated by the best case __hashy_probe() complexity.

            Worst Case Complexity: O(n^2 * k)
            While setting a value in the hash table, the __setitem__() magic method of LazyDoubleTable is invoked,
            where the position of the statistic key is found by invoking __hashy_probe() method, the worst case of __hashy_probe() method when is_insert = True
            is O(n * k). Worst case in __hashy_probe() method is when adding a new key, all the reachable slots by stepping already have an item,
            except when an empty position/DeletedItemObject is found at the last iteration of iterating the items in the table.
            Worst case of __setitem__() method happens when the hash table requires rehashing after adding an item, the worst case of __rehash() method is O(n^2 * k).
            Thus, the overall complexity is dominated by the __rehash() complexity, ie. O(n * k) + O(n^2 * k) = O(n^2 * k).
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
            n = number of items in the table
            k = length of the key

            Best Case Complexity: O(k)
            When __getitem__() magic method of LazyDoubleTable is invoked, the position of the statistic key is found by invoking __hashy_probe() method,
            the best case of __hashy_probe() method when is_insert = False is O(k).
            Best case in __hashy_probe() method is when searching for an existing key, the tuple storing the wanted key and value is found exactly at the hash position of the key without probing,
            Thus, the overall complexity of __getitem__() is dominated by the best case of __hashy_probe() complexity

            Worst Case Complexity: O(n * k)
            When __getitem__() magic method of LazyDoubleTable is invoked, the position of the statistic key is found by invoking __hashy_probe() method,
            the worst case of __hashy_probe() method when is_insert = False is O(n * k).
            Worst case in __hashy_probe() method is when all the reachable slots by stepping do not have the key we are searching for until we reach the last iteration of iterating the items in the table.
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
            and subtracting self.birth_year takes constant time, which is independent of any input size. Thus, O(1).
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
            f"Position: {self.position.name}\n"  
            f"Age: {self.get_age()}\n"
            f"Goals: {self.goals}\n"
            f"Stats: {{{stats_str}}}"
        )

    def __repr__(self) -> str:
        """ String representation of the Player object.
        Useful for debugging or when the Player is held in another data structure.
        """
        return str(self)
