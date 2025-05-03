from __future__ import annotations

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
        Initialise the Hash Table with with increments of 366 as the table size.
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
            operations as they only involve simple arithmetic operations and the total_days_of_year() method has a complexity of O(1) too.
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

        # counting the total number of days of the given date in the year
        days_of_year = self.total_days_of_year(year, month, day)

        # compute the hash value
        c = self.table_size // 366 #since the table size is a multiple of 366, thus c will be the number of years
        hash_value = ((days_of_year - 1) * c + (year % c)) % self.table_size
        return hash_value

    def total_days_of_year(self, year: int, month: int, day: int) -> int:
        """
        Method to calculate the day number of the inputted date within the year, ie. 1-366th days of a year

        Args:
            year (int): The year of the date
            month (int): The month of the date
            day (int): The day of the date

        Returns:
            int: The day number within the year

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            The best case is when month= 1 thus it won't enter the for loop. Worst case is when month = 12 and the loop will iterate 11 times which is still a fixed constant
            Therefore, both the best and worst case are the same because defining a tuple with fixed lengths, invoking is_leap_year() method and
            the loop which iterates a fixed number of times by adding the days together are all constant time operations. Thus, O(1).
        """
        # total days in each month in a normal year
        days_per_month = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

        #total days in each month in a leap year, where feb = 29 days
        if self.is_leap_year(year):
            days_per_month = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

        days_of_year = 0

        #summing all the days in each month until the month date given
        for m in range(month - 1):
            days_of_year += days_per_month[m]
        days_of_year += day

        return days_of_year

    def is_leap_year(self, year: int) -> bool:
        """
        Method to check if a year is a leap year or not

        Args:
            year (int): The year to be checked

        Returns:
            bool: True if the year is a leap year, False otherwise

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            The best and worst case are the same because this method checks the divisibility condition for leap years which only involves
            arithmetic integer comparison and modulo operations only, which are constant time operations, therefore the complexity is constant, O(1)
        """
        if year % 400 == 0:
            return True
        elif year % 100 == 0:
            return False
        elif year % 4 == 0:
            return True
        else:
            return False
