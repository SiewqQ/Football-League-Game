from __future__ import annotations

from data_structures.referential_array import ArrayR
from data_structures.abstract_hash_table import HashTable
from typing import TypeVar


V = TypeVar('V')

class DeletedItem:
    pass

class LazyDoubleTable(HashTable[str, V]):
    """
    Lazy Double Table uses double hashing to resolve collisions, and implements lazy deletion.

    Feel free to check out the implementation of the LinearProbeTable class if you need to remind
    yourself how to implement the methods of this class.

    Type Arguments:
        - V: Value Type.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = (5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869)
    HASH_BASE = 31

    def __init__(self, sizes = None) -> None:
        """
        No complexity analysis is required for this function.
        Do not make any changes to this function.
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes

        self.__size_index = 0
        self.__array: ArrayR[tuple[str, V]] = ArrayR(self.TABLE_SIZES[self.__size_index])
        self.__length = 0

    @property
    def table_size(self) -> int:
        return len(self.__array)

    def __len__(self) -> int:
        """
        Returns the number of elements in the hash table
        """
        return self.__length

    def keys(self) -> ArrayR[str]:
        """
        Returns all keys in the hash table.
        :complexity: O(N) where N is the table size.
        """
        res = ArrayR(self.__length)
        i = 0
        for x in range(self.table_size):
            if self.__array[x] is not None:
                res[i] = self.__array[x][0]
                i += 1
        return res

    def values(self) -> ArrayR[V]:
        """
        Returns all values in the hash table.

        :complexity: O(N) where N is the table size.
        """
        res = ArrayR(self.__length)
        i = 0
        for x in range(self.table_size):
            if self.__array[x] is not None:
                res[i] = self.__array[x][1]
                i += 1
        return res

    def __contains__(self, key: str) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See __getitem__.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> V:
        """
        Get the value at a certain key

        :complexity: See hashy probe.
        :raises KeyError: when the key doesn't exist.
        """
        position = self.__hashy_probe(key, False)
        return self.__array[position][1]

    def is_empty(self) -> bool:
        return self.__length == 0

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular
        order).
        """
        result = ""
        for item in self.__array:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result

    def hash(self, key: str) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.
        k = length of the key
        :complexity: O(k)
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def gcd (self, a: int, b: int)-> int:
        """
            Computes the greatest common divisor (GCD) of two integers using the Euclidean algorithm.

            Args:
                a: First integer
                b: Second integer

            Returns:
                int: GCD of a and b

            Complexity:
                According to Ed, complexity of the code for co-prime checking is free to be omitted.
            """
        while b != 0:
            a, b = b, a % b

        # when b becomes 0, a is the GCD
        return a

    def hash2(self, key: str) -> int:
        """
        Used to determine the step size for our hash table.

        Args:
            key: The key to hash

        Returns:
            int: the step size

        Complexity:
            k = length of the key

            Best Case Complexity: O(k)
            Worst Case Complexity: O(k)

            Both the best and worst case is O(k) because the complexity is dominated by the for loop which iterates over every character in the key,
            that depends on the length of key. The remaining code performs fixed arithmetic operations which are constant time operations, ie. O(1)
            therefore O(k) dominates this method.
        """
        value = 0
        a = 27449   # a large prime number, large prime can spread out step sizes
        prime_multiplier = 92821 # class variable hash base is too small, step sizes might repeat too quickly

        for char in key:
            value = (ord(char) + a * value) % (self.table_size - 1) # the second hash function
            a = (a * prime_multiplier) % (self.table_size - 1) # don't use same hash base to introduce independency from hash() method

        step = max(1, value) #double hashing by different step size, step size cant be 0

        while self.gcd(step, self.table_size) != 1: #to ensure step size coprime w table size
            step = (step + 1) % self.table_size
        return step

    def __hashy_probe(self, key: str, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using hashy probing.

        Args:
            key: The key to hash
            is_insert: True when adding a new key, False when searching for an existing key

        Returns:
            int: when is_insert = True: return the empty position where the new key will be added to
                 when is_insert = False: return the position of the found existing key

        Raises:
            KeyError: When the key is not in the table, but is_insert is False.
            RuntimeError: When a table is full and cannot be inserted.

        Complexity:
            k = length of the key
            n = number of items in the table

            Best Case Complexity: O(k)
            The hash position and step size of the inputted key is computed by primary hash and secondary hash method, which has a complexity of both O(k).
            When is_insert = False, best case is when searching for an existing key, the tuple storing the wanted key and value is found exactly at the hash position of the key without probing,
            in the else case of the for loop. Thus, the loop will iterate once only as the inputted key is found after comparing the key in the table to the inputted key string, hence the K factor.
            This analysis is assuming k is representing an average key length, and is being used as the cost of comparing two keys as well as cost of hashing a key.
            Since cost of comparing a key to another key string is equal to the cost of hashing the key. Therefore, O(1) * O(comp(str)) = O(1) * O(k).
            Thus, the overall best complexity for when is_insert = False is O(k) + O(k) + ( O(1) * O(k) ) =  O(k).
            When is_insert = True, best case is when adding a new key, an empty position is found exactly at the hash position of the key without probing, where no collision occur,
            in the elif case of the for loop. Thus, the loop will iterate once only as the loop will return the empty position immediately. Thus, O(1) * O(1) = O(1).
            Therefore, the overall best complexity for when is_insert = True is O(k)+ O(k) + (O(1)) = O(k) too.

            Worst Case Complexity: O(n * k)
            The hash position and step size of the inputted key is computed by primary hash and secondary hash method, which has a complexity of both O(k).
            When is_insert = False, worst case is when all the reachable slots by stepping do not have the key we are searching for until we reach the position that is lastly stepped, ie. we reach the last iteration of iterating items in the table
            When is_insert = True, worst case is when adding a new key, all the reachable slots by stepping already have an item except when an empty position/DeletedItemObject is found at the last iteration of iterating items in the table,
            Thus, the loop will iterate through all the items in the hash table due to collisions, as the key we are finding/ empty slot is at the position which is stepped lastly. Thus, O(n).
            At each position, the key in the table is compared to the inputted key string, hence the K factor.
            This analysis is assuming k is representing an average key length, and is being used as the cost of comparing two keys as well as cost of hashing a key.
            Since cost of comparing a key to another key string is equal to the cost of hashing the key. Therefore, O(n) * O(comp(str)) = O(n) * O(k).
            Thus, the overall worst complexity for when is_insert = False and is_insert = True is O(k) + O(k) + ( O(n) * O(k) ) = O(n * k)
        """
        # finding the position where the key will be hashed to and the step size
        position = self.hash(key)
        step = self.hash2(key)

        deleted_status = None #to rmb the first deleted slot for possible reuse when inserting

        for _ in range(self.table_size):
            current_item = self.__array[position]

            #check if an item is deleted first
            if current_item is DeletedItem:
                if is_insert and deleted_status is None:
                    deleted_status = position  # remember first deleted slot

            elif current_item is None:
                if is_insert:
                    if deleted_status is not None:
                        return deleted_status # to reuse the deleted item's space
                    else:
                        return position
                else: # when searching for item
                    raise KeyError(f"Key {key} not found")

            # current_item is a tuple (key, value)
            else:
                if current_item[0] == key:
                    return position

            #move to the next slot, adding step size computed from hash 2
            position = (position + step) % self.table_size

        #at this point, ald loop through all the hash table but still not yet find a position for key yet
        if is_insert:
            raise RuntimeError("Table is full")

        #if searching:
        raise KeyError(f"Key {key} not found")

    def __setitem__(self, key: str, data: V) -> None:
        """
        Set a (key, value) pair in our hash table.

        Remember! This is where you will need to call __rehash if the table is full!

        Args:
            key: The key to hash
            data: The data of the key

        Returns:
            None

        Complexity:
            k = length of the key
            n = number of items in the table

            Best Case Complexity: O(k)
            While setting an item in a hash table, the position of the key is found by invoking __hashy_probe() method, the best case of __hashy_probe() method when is_insert = True
            is O(k). Best case in __hashy_probe() is when adding a new key, an empty position is found exactly at the hash position of the key without probing, where no collision occurs.
            Thus, the overall best complexity is dominated by the __hashy_probe() complexity, O(k), where no rehashing is required.

            Worst Case Complexity: O(n^2 * k)
            While setting an item in a hash table, the position of the key is found by invoking __hashy_probe() method, the worst case of __hashy_probe() method when is_insert = True
            is O(n * k). Worst case in __hashy_probe() method is when adding a new key, all the reachable slots by stepping already have an item,
            except when an empty position/DeletedItemObject is found at the last iteration of iterating the items in the table.
            Worst case of __setitem__() method happens when the hash table requires rehashing after adding an item, the worst case of __rehash() method is O(n^2 * k).
            Thus, the overall complexity is dominated by the __rehash() complexity, ie. O(n * k) + O(n^2 * k) = O(n^2 * k)
        """
        position = self.__hashy_probe(key, True)

        # new key can be added, update length first
        if self.__array[position] is None or self.__array[position] is DeletedItem:
            self.__length += 1

        # adding (setting) new key data value / updating data if key ald exist
        self.__array[position] = (key, data)

        # Check if we need to rehash after adding an item
        if self.__length > self.table_size * 2 / 3 and self.__size_index < len(self.TABLE_SIZES) - 1:
            self.__rehash()

    def __delitem__(self, key: str) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        Args:
            key: The key to hash

        Returns:
            None

        Complexity:
            k = length of the key
            n = number of items in the table

            Best Case Complexity: O(k)
            The position of the to be deleted item is found using __hashy_probe() method where the best case is O(k).
            Best case of __hashy_probe() when is_insert = False, is when searching for an existing key,
            the tuple storing the wanted key and value is found exactly at the hash position of the key without probing, where no collision occurs.
            Thus, the overall complexity is dominated by the best case of __hashy_probe() method ie, O(k).

            Worst Case Complexity: O(n * k)
            The position of the to be deleted item is found using __hashy_probe() method where the worst case is O(n * k).
            Worst case of __hashy_probe() when is_insert = False, is when searching for an existing key, all the reachable slots by stepping do not have the key we are searching for
            until we reach the last iteration of iterating the items in the table.
            Thus, the overall complexity is dominated by the worst case of __hashy_probe() method ie, O(n * k).
        """
        position = self.__hashy_probe(key, False)
        self.__array[position] = DeletedItem
        self.__length -= 1

    def __rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Args:
            None

        Returns:
            None

        Complexity:
            k = length of the key
            n = number of items in the table

            Best Case Complexity: O(n * k)
            while copying all the items in the old array to the new array,the for loop will iterate n times,
             __setitem__() magic method is invoked while assigning new key value pair in the new array, which will invoked the __hashy_probe() method also.
            The best case of __hashy_probe() when is_insert = True is O(k),
            where when adding a new key, an empty position is found exactly at the hash position of the key without probing, where no collision occurs.
            In this case, it means all items can be inserted immediately after being hashed with no probing needed.
            Thus, the overall complexity is O(n) * O(k) = O(n * k)

            Worst Case Complexity: O(n^2 * k)
            while copying all the items in the old array to the new array,the for loop will iterate n times,
             __setitem__() magic method is invoked while assigning new key value pair in the new array, which will invoked the __hashy_probe() method also.
            The worst case of __setitem__() is not used because while rehashing, another rehash in __setitem__() will not happen as the table is already being resized.
            Thus, The worst case of __hashy_probe() in __setitem__() is used instead. The worst case of __hashy_probe() when is_insert = True is O(n * k),
            where when all items need maximum probing to be inserted in the new table.
            Thus, the overall complexity is O(n) * O(n * k) = O(n^2 * k)
        """
        old_array = self.__array

        self.__size_index += 1 #moving to the next table size
        self.__array = ArrayR(self.TABLE_SIZES[self.__size_index])

        self.__length = 0

        for item in old_array:
            if item is not None and item is not DeletedItem:
                key, value = item
                self[key] = value
