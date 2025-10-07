from __future__ import annotations
from datetime import datetime
from data_structures.hash_table_linear_probing import LinearProbeTable


class HashyDateTable(LinearProbeTable[str]):
    """
    HashyDateTable assumed the keys are strings representing dates, and therefore tries to
    produce a balanced, uniform distribution of keys across the table.

    Conflicts are resolved using Linear Probing.

    All values will also be strings.
    """
    def __init__(self) -> None:
        """
        Initialise the Hash Table with increments of 366 as the table size.
        This means, initially we will have 366 slots, once they are full, we will have 4 * 366 slots, and so on.

        No complexity is required for this function.
        Do not make any changes to this function.
        """
        LinearProbeTable.__init__(self, [366, 4 * 366, 16 * 366])

    def hash(self, key: str) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.
        The key will always be exactly 10 characters long and can be any of these formats, but nothing else:
        - DD/MM/YYYY
        - DD-MM-YYYY
        - YYYY/MM/DD
        - YYYY-MM-DD

        The function assumes the dates will always be valid.

        Args:
            key (str): The key to hash.

        Returns:
            int: The hash value.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            The best case and worst case are the same because checking the format of the date, parsing and computing the hash value are constant time
            operations as they only involve simple arithmetic operations. According to Ed, any use of the datetime library's methods is assumed to have O(1) complexity.
            The function of timetuple() method is explained here: https://www.geeksforgeeks.org/timetuple-function-of-datetime-date-class-in-python/
            Thus, the overall complexity is O(1).
        """
        # parsing the year, month and day based on the format of the date
        if key[4] == '-' or key[4] == '/':
            # when the format is YYYY-MM-DD or YYYY/MM/DD
            year = int(key[0:4])
            month = int(key[5:7])
            day = int(key[8:10])
        else:
            # when the format is DD-MM-YYYY or DD/MM/YYYY
            day = int(key[0:2])
            month = int(key[3:5])
            year = int(key[6:10])

        # joins the day, month, and year into one date object that can correctly handle things like leap years and different month lengths, using the datetime library.
        date_obj = datetime(year, month, day)
        days_of_year = date_obj.timetuple().tm_yday # timetuple().tm_yday returns the day of the year based on the date object

        # computing the hash value
        c = self.table_size // 366 #since the table size is a multiple of 366, thus c will be the number of years
        hash_value = ((days_of_year - 1) * c + (year % c)) % self.table_size # -1 as hash table position starts from 0

        return hash_value

