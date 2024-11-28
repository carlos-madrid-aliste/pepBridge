import csv
import os
import sys
import pprint
import numpy as np
    
class MALDI_LCMS:
    """
    A class to manage and process LCMS or MALDI data.

    This class reads configuration files, loads LCMS/MALDI data from CSV files,
    processes it, and provides functionalities to manipulate and analyze the data.
    
    """
    
    def __init__(self, ini_file, debug=False) -> None:
        """
        Initialize the MALDI_LCMS object.

        Args:
            config_file (str): Path to the configuration file.
            debug (bool)     : Enable debugging messages if True.

        Raises:
            FileNotFoundError: If the config file cannot be found.
        """

        # Since config_file is part of the pepBridge package, you should use a 
        # relative import to ensure Python looks for it within the same package 
        # rather than as an external module     
        #import config_file as cfg
        from .config_file import config_file

        
        self.debug = debug
        self.data  = list()        # List of dictionaries containing LCMS/MALDI data
        self.ordered_file = list() # Data ordered for display, as specified by the user.
        self.column_names = list()
    
        cfg_obj = config_file(location=ini_file, debug=self.debug)
        cfg_obj.read_ini()
        
        self.file_name = cfg_obj.get_file_name()
        self.round_mz  = cfg_obj.get_round_mz()
        
        # name of the column holding the rounded M/Z
        self.rounded_column_name = cfg_obj.get_rounded_column_name()
        self.mz_column_name      = cfg_obj.get_mz_column_name()

        self.verbose      = cfg_obj.get_verbose()
        self.output_file  = cfg_obj.get_output_file()
        self.column_names = cfg_obj.get_column_names()
        self.order_columns= cfg_obj.get_order_columns()
        
        if self.debug:
            print(f"This is the constructor. round_mz = {self.round_mz}, order_columns = {self.order_columns}")
        
    def get_ordered_columns(self):
        """ get_ordered_columns:
            Returns the list of ordered columns as specified by the user.
        """
        return self.order_columns
    
    def get_column_names(self):
        """ get_column_names:
            Returns the list of all column names in the dataset.
        """
        return self.column_names
    
    def get_mass_for_search(self):
        """ get_mass_for_search:
        Determines which column (rounded or unrounded) to use for mass comparison.

        Returns:
            str: The name of the column used for mass comparison.

        Raises:
            ValueError: If no valid column name is found.
        """    
        column_name=None
        if self.round_mz:
            column_name = self.rounded_column_name
        else:
            column_name = self.mz_column_name
        
        if column_name is None:
            raise ValueError("Column name for mass search is not defined.")
        return column_name

    def locate_mz(self):
        """
        Finds the position of the column used for mass comparison in the ordered columns.
            
            if value in the round_mz section is set to True
            [round_mz]
            value=True
            column_name=rounded_mz
        
            then the rounded_mz will be used for comparison. Otherwise the 
            column specified in the mz_column_name section.
            
            [mz_column_name]
            name=m/z
        Returns:
            int: Index of the column in the ordered columns list.
        """
        if self.debug:
            print(f"self.round_mz = {self.round_mz}")
            print(f"self.mz_column_name = {self.mz_column_name}")
        
        
        # the index() method returns the index of the specified
        # element in the list. If the element is not found, a 
        # ValueError exception is raised.   
        column_name = self.get_mass_for_search()
        try:
            index = self.order_columns.index(column_name)
            if self.debug:
                print(f"located_mz column_name = {column_name}")    
            return index
        except ValueError:
            raise ValueError(f"Column '{column_name}' not found in the ordered columns.")  

    def load(self):
        """
        Loads LCMS/MALDI data from the specified CSV file and add the rounded column.

        Rounds the m/z values if specified in the configuration.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        import csv
        import sys
        
        if not os.path.exists(self.file_name):
            raise FileNotFoundError(f"File '{self.file_name}' not found.")

        with open(self.file_name, mode='r', encoding='utf-8-sig' ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # round_mz = 1, it will round the LCMS m/z to the nearest integer.
                if self.round_mz:
                    row[self.rounded_column_name] = round(float(row[self.mz_column_name]))
                self.data.append(row)
        
        if self.debug:
            print(f"Loaded data with {len(self.data)} rows from {self.file_name}")
        
    
    def get_file(self):
        """
        Converts the LCMS or MALDI internal data structure into a list of lists 
        based on ordered columns.

        Returns:
            list: Data ordered as specified by the user.
            
            File is returned in the order specified by the user in the [order_columns] field.
        """
        
        for my_dict in self.data:
            row = [my_dict[column_name] for column_name in self.order_columns]
            self.ordered_file.append(row)
        return self.ordered_file
            
    def to_lol(self):
        """
        Converts a list of dictionaries to a list of list.
        input:
            list of dictionaries represent a LCMS or MALDI file.
        """
        for my_dict in self.data:
            #print(my_dict)
            # get the values for each LCMS column_name
            my_tmp = list()
            for column_name in self.order_columns:
                column_value = my_dict[column_name]
                my_tmp.append(column_value)
            self.lcms_file.append(my_tmp)    
        return self.lcms_file
            
    @classmethod
    def equal_lists(cls, rounded_column_name, list1, list2, not_include_rounded_mz=True)->bool:
        # creating a cloning of the list. 
        # The original list remains unchanged.
        my_list1 = list1[:]
        my_list2 = list2[:]
        
        # removing the 'rounded m/z' from both lists.
        if rounded_column_name in my_list1:
            my_list1.remove(rounded_column_name)
        
        if rounded_column_name in my_list2:
            my_list2.remove(rounded_column_name)
        
        my_list1.sort()
        my_list2.sort()
        
        if (my_list1 == my_list2):
            return True
        else:
            return False

    def extract_mz(self):
        """
        Extracts the m/z values from the loaded data (MALDI or LCMS csv file).

        Returns:
            list: A list of m/z values (rounded or unrounded based on the configuration).
            
            To extract a rounded to the nearest m/z set value=True in the ini 
            file. Please see below:
            
            [round_mz]
            value=True
            column_name=rounded_mz
        """
        
        # self.data hold a list of dictionaries
        '''
        [
        {'196a Thymus (Left) Chemo': '-1.19564044324931',
        '196a Thymus (Right) No Chemo': '-1.48359079194966',
        'Annotated Sequence': '[R].HLVPGAGGEAGEGDPGGAGDYGNGLESEELEPGELLPEPEPEEEPPRPR.[A]',
        'Gene Name': 'Pabpn1',
        'Master Protein Accessions': 'Q8CCS6',
        'Master Protein Descriptions': 'Polyadenylate-binding protein 2 OS=Mus '
                                 'musculus OX=10090 GN=Pabpn1 PE=1 SV=3',
        'Modifications': '1xDeamidated [N23]',
        'Rounded mz': 4990,
        'Theo. MH+ [Da]': '4990.27733'}, ..... ]
        '''
        
        if not self.data:
            raise ValueError("Data has not been loaded. Call the 'load()' method first.")
            #sys.exit()
        
        # pick what columns to return. The one that is rounded or not.
        column_name = self.rounded_column_name if self.round_mz else self.mz_column_name
        return [my_dict[column_name] for my_dict in self.data]
    
    def write(self, output_file, include_rounded_mz=False):
        """
        Writes the processed data to a CSV file.

        Args:
            output_file (str): Path to the output CSV file.
            include_rounded_mz (bool): Whether to include the rounded m/z column in the output.
        """
        
        csv_headers = self.column_names
        if include_rounded_mz and self.rounded_column_name not in csv_headers:
            csv_headers.insert(1, self.rounded_column_name)
        
        if self.debug:
            print(csv_headers)
        
        with open(output_file, mode='w', newline='') as data_file:
            dwriter = csv.DictWriter(data_file, dialect='excel', fieldnames=csv_headers)
            dwriter.writeheader()

            for my_dict in self.data:
                if include_rounded_mz == False and self.rounded_column_name in my_dict:
                    del my_dict[self.rounded_column_name] 
                dwriter.writerow(my_dict)
    
if __name__ == "__main__":
    import MatchingMZ as mm
   
    config_file = 'lcms.ini'
    lcms_obj = MALDI_LCMS(config_file=config_file, debug=False) 
    
    lcms_obj.load() 
    
    # mz = lcms_obj.extract_mz()
    # line = lcms_obj.get_file()
    print (f"*** LCMS ***")
    print (f"column_names    = {lcms_obj.get_column_names()}")
    print (f"ordered_columns = {lcms_obj.get_ordered_columns()}")
    print (f"mass_for_search = {lcms_obj.get_mass_for_search()}")
    print (f"Index of the searching mass [m/z] = {lcms_obj.locate_mz()} in ordered_columns")
    
    # Write to a file
    lcms_obj.write('output_file4.csv', include_rounded_mz=False)
    
    maldi_ini_file = 'maldi.ini'
    maldi_obj = MALDI_LCMS(config_file=maldi_ini_file, debug=False) 
    maldi_obj.load() 
    
    print()
    print (f"*** MALDI ***")
    print (f"column_names    = {maldi_obj.get_column_names()}")
    print (f"ordered_columns = {maldi_obj.get_ordered_columns()}")
    print (f"mass_for_search = {lcms_obj.get_mass_for_search()}")
    print (f"Index of the searching mass [m/z] = {maldi_obj.locate_mz()} in ordered_columns")
    
    
    mz = maldi_obj.extract_mz()
    
