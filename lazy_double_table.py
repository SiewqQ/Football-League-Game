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
        :complexity: O(N) where N is the number of items in the table.
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

        :complexity: O(N) where N is the number of items in the table.
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
        :complexity: O(len(key))
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def gcd (self, a: int, b: int)-> bool:
        """
            Computes the greatest common divisor (GCD) of two integers using the Euclidean algorithm.

            Args:
                a: First integer
                b: Second integer

            Returns:
                int: GCD of a and b

            Complexity:
                According to ed, complexity of the code for co-prime checking is free to be omitted.
            """
        while b != 0:
            a, b= b, a % b

        #when b becomes 0, a is the GCD
        return a

    def hash2(self, key: str) -> int:
        """
        Used to determine the step size for our hash table.

        Args:
            key: The key to hash

        Returns:
            int: the step size

        Complexity:
            Best Case Complexity: O(len(key))
            Worst Case Complexity: O(len(key))

            Both the best and worst case is O(len(key)) because the complexity is dominated by the for loop which iterates over every character in the key,
            that depends on the length of key. The remaining code performs fixed arithmetic operations which are constant time operations, ie. O(1)
            therefore O(len(key)) dominates this method.
        """
        value = 0
        a = 27449   # a large prime number
        for char in key:
            value = (ord(char) + a * value) % (self.table_size - 1) # the second hash function
            a = (a * (self.HASH_BASE + 2)) % (self.table_size - 1) # using a different hash base by adding 2 to it

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
            n = the table size

            Best Case Complexity: O(len(key))
            The hash position and step size of the inputted key is computed by primary hash and secondary hash, which has a complexity of both O(len(key)).
            When is_insert = False, best case is when searching for an existing key, the tuple storing the wanted key and value is found exactly at the hash position of the key without probing,
            ie. the else case of the for loop. Thus, the loop will iterate once only as the key is found after comparing the key in the table to the inputted key string. Therefore, O(1) * O(comp(str)).
            Thus, the overall best complexity for when is_insert = False is O(len(key)) + O(len(key)) + ( O(1) * O(comp(str)) ) =  O(len(key) + comp(str)).
            Since cost of comparing the key to another string is equal to the cost of hashing the key, thus the overall complexity is O(len(key) + comp(str)) = O(len(key)).
            When is_insert = True, best case is when adding a new key, an empty position is found exactly at the hash position of the key where no collision occur,
            ie. entering the elif case of the for loop. Thus, the loop will iterate once only as the loop will return the empty position immediately. Thus, O(1) * O(1) = O(1).
            Therefore, the overall best complexity for when is_insert = True is O(len(key))+ O(len(key)) + (O(1)) = O(len(key))

            Worst Case Complexity: O(len(key) + n * comp(str))
            The hash position and step size of the inputted key is computed by primary hash and secondary hash, which has a complexity of both O(len(key)).
            When is_insert = False, worst case is when all the reachable slots by stepping do not have the key we are searching for until the position that is lastly stepped, ie. we reach the last iteration of iterating the table size
            When is_insert = True, worst case is when adding a new key, all the reachable slots by stepping already have an item except when an empty position/DeletedItemObject is found at the last iteration of iterating table size,
            This cause the for loop to loop through the items in hash table due to collisions, no matter the item is a DeletedItem object or a tuple containing key and value
            that involves comparison of the key in the table and inputted key string, ie. O(comp(str)) too.
            Thus, the loop will iterate the entire table size as the key we are finding/ empty slot is at the position which is stepped lastly. Thus, O(n).
            At each iteration, the key in the table is compared to the inputted key string, ie. O(comp(str)). Therefore, the overall complexity of this loop is O(n) * O(comp(str)).
            Thus, the overall worst complexity for when is_insert = False and is_insert = True is O(len(key)) + O(len(key)) + ( O(n) * O(comp(str)) ) =  O(len(key) + n * comp(str)).
        """
        # finding the position where the key will be hashed to and the step size
        position = self.hash(key)  #O(len(key))
        step = self.hash2(key) #O(len(key))
        first_deleted = None #to rmb the first deleted slot for possible reuse when inserting

        for _ in range(self.table_size): #O(n)
            current_item = self.__array[position]

            #check if an item is deleted first
            if current_item is DeletedItem:
                if is_insert and first_deleted is None:
                    first_deleted = position  # remember first deleted slot

            elif current_item is None:
                if is_insert:
                    if first_deleted is not None:
                        return first_deleted
                    else:
                        return position
                else: # when searching for item
                    raise KeyError(f"Key {key} not found")

            # current_item is a tuple (key, value)
            else:
                if current_item[0] == key: #O(comp(str))
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
            n = the table size

            Best Case Complexity: O(len(key))
            While setting an item in a hash table, the position of the key is found by invoking __hashy_probe() method, the best case of __hashy_probe() method when is_insert = True
            is O(len(key)). Best case in __hashy_probe() is when adding a new key, an empty position is found exactly at the hash position of the key where no collision occurs.
            Thus, the overall best complexity is dominated by the __hashy_probe() complexity, O(len(key)), where no rehashing is required.

            Worst Case Complexity: O(n * len(key) + n^2 * comp(str))
            While setting an item in a hash table, the position of the key is found by invoking __hashy_probe() method, the worst case of __hashy_probe() method when is_insert = True
            is O(len(key) + n * comp(str)). Worst case in __hashy_probe() method is when adding a new key, all the reachable slots by stepping already have an item,
            except when an empty position/DeletedItemObject is found at the last iteration of iterating table size, this cause the for loop to loop through the items in hash table due to collisions.
            Worst case of __setitem__() method happens when the hash table requires rehashing after adding an item, the worst case of __rehash() method is O(n * len(key) + n^2 * comp(str)).
            Thus, the overall complexity is dominated by the __rehash() complexity, ie. (O(len(key) + n * comp(str))) + (O(n * len(key) + n^2 * comp(str))) = O(n * len(key) + n^2 * comp(str))
        """
        position = self.__hashy_probe(key, True) # best: O(len(key)), worst: O(len(key) + n * comp(str))

        # adding new key
        if self.__array[position] is None or self.__array[position] is DeletedItem:
            self.__length += 1

        # updating data
        self.__array[position] = (key, data)

        # Check if we need to rehash after adding an item
        if (self.__length + 1) > self.table_size * 2 / 3 and self.__size_index < len(self.TABLE_SIZES) - 1:
            self.__rehash() #best: O(n * len(key)), worst: O(n * len(key) + n^2 * comp(str))

    def __delitem__(self, key: str) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        Args:
            key: The key to hash

        Returns:
            None

        Complexity:
            n = the table size

            Best Case Complexity: O(len(key))
            The position of the to be deleted item is found using __hashy_probe() method where the best case is O(len(key)).
            Best case of __hashy_probe() when is_insert = False, is when searching for an existing key,
            the tuple storing the wanted key and value is found exactly at the hash position of the key without probing,
            Thus, the overall complexity is dominated by the best case of __hashy_probe() method ie, O(len(key)).

            Worst Case Complexity: O(len(key) + n * comp(str))
            The position of the to be deleted item is found using __hashy_probe() method where the worst case is O(len(key) + n * comp(str)).
            Worst case of __hashy_probe() when is_insert = False, is when searching for an existing key, all the reachable slots by stepping do not have the key we are searching for
            until we reach the last iteration of iterating the table size this cause the for loop to loop through the items in hash table due to collisions.

            Thus, the overall complexity is dominated by the worst case of __hashy_probe() method ie, O(len(key) + n * comp(str)).
        """
        position = self.__hashy_probe(key, False)  # best: O(len(key)), worst: O(len(key) + n * comp(str))
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
            n = len(self), ie. the number of items in the current array

            Best Case Complexity: O(n * len(key))
            while copying all the items in the old array to the new array,the for loop will iterate n times,
             __setitem__() magic method is invoked while assigning new key value pair in the new array, which will invoked the __hashy_probe() method also.
            The best case of __hashy_probe() when is_insert = True is O(len(key)),
            when adding a new key, an empty position is found exactly at the hash position of the key where no collision occurs.
            Thus, the overall complexity is O(n) * O(len(key)) = O(n * len(key))

            Worst Case Complexity: O(n * len(key) + n^2 * comp(str))
            while copying all the items in the old array to the new array,the for loop will iterate n times,
             __setitem__() magic method is invoked while assigning new key value pair in the new array, which will invoked the __hashy_probe() method also.
            The worst case of __hashy_probe() when is_insert = True is O(len(key) + n * comp(str)),
            when adding a new key, all the reachable slots by stepping already have an item, except an empty position/DeletedItemObject is found at the last iteration,
            this cause the for loop to loop through the items in hash table due to collisions.
            Thus, the overall complexity is O(n) * O(len(key) + n * comp(str)) = O(n * len(key) + n^2 * comp(str))
        """
        old_array = self.__array

        self.__size_index += 1 #moving to the next table size

        if self.__size_index >= len(self.TABLE_SIZES):
            raise RuntimeError("Table is full")

        self.__array = ArrayR(self.TABLE_SIZES[self.__size_index]) # O(m), m= new table size
        self.__length = 0

        for item in old_array: #O(n)
            if item is not None and item is not DeletedItem:
                key, value = item
                self[key] = value #calls set item, calls hashy probe, use hashy best worst not setitem, # best: O(len(key)), worst :O(hash(key) + N*comp(str))
