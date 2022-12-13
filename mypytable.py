from configparser import DuplicateOptionError
import copy
import csv
from tabulate import tabulate 
import statistics

# install tabulate with: pip install tabulate

# required functions/methods are noted with TODOs
# provided unit tests are in test_mypytable.py
# do not modify this class name, required function/method headers, or the unit tests
class MyPyTable:
    """Represents a 2D table of data with column names.
    Attributes:
        column_names(list of str): M column names
        data(list of list of obj): 2D data structure storing mixed type data.
            There are N rows by M columns.
    """

    def __init__(self, column_names=None, data=None):
        """Initializer for MyPyTable.
        Args:
            column_names(list of str): initial M column names (None if empty)
            data(list of list of obj): initial table data in shape NxM (None if empty)
        """
        if column_names is None:
            column_names = []
        self.column_names = copy.deepcopy(column_names)
        if data is None:
            data = []
        self.data = copy.deepcopy(data)

    
    def pretty_print(self):
        #Prints the table in a nicely formatted grid structure.
        
        print(tabulate(self.data, headers=self.column_names))
    
    
    def get_shape(self):

        """Computes the dimension of the table (N x M).
        Returns:
            int: number of rows in the table (N)
            int: number of cols in the table (M)
        """
        row_n = len(self.data)
        col_m = len(self.data[0])

        return row_n, col_m

    def get_column(self, col_identifier, include_missing_values=True):
        """Extracts a column from the table data as a list.
        Args:
            col_identifier(str or int): string for a column name or int
                for a column index
            include_missing_values(bool): True if missing values ("NA")
                should be included in the column, False otherwise.
        Returns:
            list of obj: 1D list of values in the column
        Notes:
            Raise ValueError on invalid col_identifier
        """
        index = -1

        for i in range(len(self.column_names)):
            if col_identifier == self.column_names[i]:
                index = i
        
        for i in range(len(self.data)):
            if self.data[i][index] == "NA":
                include_missing_values = True
            else:
                include_missing_values = False
    
        my_list = []

        for i in self.data:
            my_list.append(i[index])

        return my_list

    def convert_to_numeric(self):
        """Try to convert each value in the table to a numeric type (float).
        Notes:
            Leave values as is that cannot be converted to numeric.
        """
        for table in self.data:
            for i in range(len(table)):
                try:
                    convert = float(table[i])
                    table[i] = convert
                except ValueError:
                    pass


    def drop_rows(self, row_indexes_to_drop):
        """Remove rows from the table data.
        Args:
            row_indexes_to_drop(list of int): list of row indexes to remove from the table data.
        """
        # row = self.data

        final_list = []

        for i in range(len(self.data)):
            if i not in row_indexes_to_drop:
                final_list.append(self.data[i])

        self.data = final_list
        

    def load_from_file(self, filename):
        """Load column names and data from a CSV file.
        Args:
            filename(str): relative path for the CSV file to open and load the contents of.
        Returns:
            MyPyTable: return self so the caller can write code like
                table = MyPyTable().load_from_file(fname)
        Notes:
            Use the csv module.
            First row of CSV file is assumed to be the header.
            Calls convert_to_numeric() after load
        """

        self.data = []
        with open(filename, 'r', encoding='utf-8') as file:
            csvreader = csv.reader(file)
            self.column_names = next(csvreader)
            for row in csvreader:
                self.data.append(row)

        '''
        i = 0
        with open(filename, "r") as infile:
            self.data = []
            self.column_names = []
            for line in infile:
                words = line.strip().split(',')
                if i == 0:
                    self.column_names = (words)
                    i = i + 1 
                else:
                    self.data.append(words)
        infile.close()
        '''
        self.convert_to_numeric()
        return self

    def save_to_file(self, filename):
        """Save column names and data to a CSV file.
        Args:
            filename(str): relative path for the CSV file to save the contents to.
        Notes:
            Use the csv module.
        """

        with open(filename, 'w', newline='') as filename:
            writer = csv.writer(filename)
            writer.writerow(self.column_names)
            for row in self.data:
                writer.writerow(row)
                
    

    def find_duplicates(self, key_column_names):
        """Returns a list of indexes representing duplicate rows.
        Rows are identified uniquely based on key_column_names.
        Args:
            key_column_names(list of str): column names to use as row keys.
        Returns
            list of int: list of indexes of duplicate rows found
        Notes:
            Subsequent occurrence(s) of a row are considered the duplicate(s).
                The first instance of a row is not considered a duplicate.
        """

        duplicate_list = []
        seen_list = []
        key_indexes = []

        for i in range(len(self.column_names)):
            if self.column_names[i] in key_column_names:
                key_indexes.append(i)
        
        for i in range(len(self.data)):
            key = []
            for j in key_indexes:
                key.append(self.data[i][j])
            if key in seen_list:
                duplicate_list.append(i)
            else:
                seen_list.append(key)

        return duplicate_list

        

        #return [] # (returning list of indexes) TODO: fix this

    def remove_rows_with_missing_values(self):
        """Remove rows from the table data that contain a missing value ("NA").
        """

        new_list = []

        for table in self.data:
            if "N/A" not in table:
                new_list.append(table)
        
        self.data = new_list
    
    def remove_rows_with_missing_values_2(self):
        """Remove rows from the table data that contain a missing value ("NA").
        """

        new_list = []

        for table in self.data:
            if '' not in table:
                new_list.append(table)
        
        self.data = new_list

        return new_list


    def replace_missing_values_with_column_average(self, col_name):
        """For columns with continuous data, fill missing values in a column
            by the column's original average.
        Args:
            col_name(str): name of column to fill with the original average (of the column).
        """
        index = -1

        for i in range(len(self.column_names)):
            if col_name == self.column_names[i]:
                index = i
        
        tot = 0.0
        count = 0
        remove_list_NAs = []

        for i in range(len(self.data)):
            if "NA" not in self.data[i]:
                tot += self.data[i][index]
                count += 1
            else:
                remove_list_NAs.append(i)

        avg_col = tot/count

        for i in remove_list_NAs:
            if self.data[i][index] == "NA":
                self.data[i][index] = avg_col
        
    
    def find_middle(self, middle_list):
        middle = (min(middle_list) + max(middle_list)) / 2
        return middle


    def compute_summary_statistics(self, col_names):
        """Calculates summary stats for this MyPyTable and stores the stats in a new MyPyTable.
            min: minimum of the column
            max: maximum of the column
            mid: mid-value (AKA mid-range) of the column
            avg: mean of the column
            median: median of the column
        Args:
            col_names(list of str): names of the numeric columns to compute summary stats for.
        Returns:
            MyPyTable: stores the summary stats computed. The column names and their order
                is as follows: ["attribute", "min", "max", "mid", "avg", "median"]
        Notes:
            Missing values should in the columns to compute summary stats
                for should be ignored.
            Assumes col_names only contains the names of columns with numeric data.
        """

        num_list = []
        dup_list = []
        empty_list = []
        tot = 0.0

        for name in col_names:
            col_info = self.get_column(name)
            num_list.append(col_info)

        c = 0

        for i in num_list:
            loop_list = []
            loop_list.append(col_names[c])
            col_info = self.get_column(col_names[c])
            tot = sum(col_info)
            length_for_avg = len(col_info)

            if length_for_avg == 0:
                empty_list.append(col_info)
            else:
                avg = tot/length_for_avg

            if col_info == []:
                empty_list.append(loop_list)
            else:
                mini = min(i)
                maxi = max(i)
                middle_actual = self.find_middle(i)
                median = statistics.median(i)
                loop_list.append(mini)
                loop_list.append(maxi)
                loop_list.append(middle_actual)
                loop_list.append(avg)
                loop_list.append(median)
                dup_list.append(loop_list)
                c += 1

        return MyPyTable(self, dup_list) # TODO: fix this
        

    def perform_inner_join(self, other_table, key_column_names):
        """Return a new MyPyTable that is this MyPyTable inner joined
            with other_table based on key_column_names.
        Args:
            other_table(MyPyTable): the second table to join this table with.
            key_column_names(list of str): column names to use as row keys.
        Returns:
            MyPyTable: the inner joined table.
        """
        # make helper functions like gina said (matching function?)
        # pre step to for loop (main part of inner join) is to figure out
        # the header first and to maintain same order
        # key column names is just product, so the self.column_names is the 
        # one that has the difference
        # seen list is where we can see the duplicates
        
        #go through every row in one table, and for each row check if its in the other table


        table_1 = []
        header_1 = []
        table_2 = []
        header_2 = []
        table_3 = []
        header_3 = []

        test_list = []

        duplicate_list = []
        seen_list = []
        key_indexes_table_1 = []
        key_indexes_table_2 = []
        

        for i in self.data:
            table_1.append(i)
        
        for i in self.column_names:
            header_1.append(i)
        
        for i in other_table.data:
            table_2.append(i)
        
        for i in other_table.column_names:
            header_2.append(i)
        
        for i in self.column_names:
            header_3.append(i)

        for i in other_table.column_names:
            if i not in key_column_names:
                header_3.append(i)

        index = -1

        for i in range(len(other_table.column_names)):
            if key_column_names == other_table.column_names[i]:
                index = i

        # KEY LOOP
         # finding duplicates
        for i in range(len(header_1)):
            if header_1[i] in key_column_names:
                key_indexes_table_1.append(i)
        
        for i in range(len(header_2)):
            if header_2[i] in key_column_names:
                key_indexes_table_2.append(i)
        # TABLE 1 LOOP
        for i in range(len(table_1)):
            key = []
            for j in key_indexes_table_1:
                key.append(table_1[i][j])
            seen_list.append(key)
            
        # TABLE 2 LOOP
        for i in range(len(table_2)):
            key = []
            for j in key_indexes_table_2:
                key.append(table_2[i][j])
            if key in seen_list:
                duplicate_list.append(table_1[i])
                duplicate_list[-1].append(table_2[i][index])
            else:
                seen_list.append(key)
    
        # end of finding duplicates

        for i in range(len(other_table.data)):
            test_list.append(other_table.data[i][index])

        for i in duplicate_list:
            table_3.append(i)

        
        my_table_index_list = []

        for label in header_3:
            if label in header_1:
                my_table_index_list.append(header_1.index(label))
        
        table = MyPyTable()
        table.data = table_3
        table.column_names = header_3

        return table # TODO: fix this

    def perform_full_outer_join(self, other_table, key_column_names):
        """Return a new MyPyTable that is this MyPyTable fully outer joined with
            other_table based on key_column_names.
        Args:
            other_table(MyPyTable): the second table to join this table with.
            key_column_names(list of str): column names to use as row keys.
        Returns:
            MyPyTable: the fully outer joined table.
        Notes:
            Pad the attributes with missing values with "NA".
        """
        return MyPyTable() # TODO: fix this