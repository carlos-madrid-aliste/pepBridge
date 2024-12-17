import os
import sys
from configparser import ConfigParser, ExtendedInterpolation

class config_file:
    def __init__(self, location, debug=False) -> None:
        """
        A class to handle reading and parsing configuration files in INI format.

        This class reads an INI file and stores configuration values in a dictionary.
        It provides methods to retrieve specific configuration parameters.
            
            Parameters:
            ----------
            location: directory path 
            debug:  optional parameter (boolean) for debbuging purposes.
                    set to False for default.
            
            Return: a config_file object.
        """
        
        self.location = location
        self.debug = debug
        self.config_values = dict()
        
        self.config_values = {
            'file_name': None,
            'round_mz': None,
            'mz_column_name': None,
            'verbose': None,
            'output_file': None,
            'column_names': None,
            'rounded_column_name': None,
            'order_columns': None
        }
        if not os.path.exists(self.location):
            sys.exit(f"Error: Configuration file '{self.location}' does not exist.")

        if self.debug:
            print(f"ConfigFile initialized for location: {self.location}")
        
        """
        We should return error if INI-like format is not provided. Add functionality
        to check if file exists and follows the INI-format and also the sections and
        values are the expected ones.
        """

    def read_ini(self):
        """
        Read and parse the INI configuration file.

        Stores the parsed values into the `config_values` dictionary.

        Raises:
            Exception: If there is an issue parsing the file or missing expected sections/keys.
        """
        
        # these two lines should be use for the reading method
        #return error if INI files does not exists.
        #assert os.path.exists(self.location) == True, f"config file {self.location} does not exists!."
        
        # reading INI file
        config = ConfigParser(interpolation=ExtendedInterpolation())
        ini_file = self.location
        config.read(ini_file)
        
        if self.debug:
            print(f"Reading INI file: {self.location}")

        try:
            # Mandatory fields
            self.config_values['file_name'] = config.get('file', 'name')
            self.config_values['mz_column_name'] = config.get('mz_column_name', 'name')
            #self.config_values['output_file'] = config.get('output_file', 'name')
            
            # Optional fields with default values
            self.config_values['round_mz'] = config.getboolean('round_mz', 'value', fallback=False)
            self.config_values['rounded_column_name'] = config['round_mz'].get('column_name', None)
            self.config_values['verbose']     = config.getboolean('verbose', 'value', fallback=False)
            self.config_values['output_file'] = config.get('output_file', 'name', fallback=None)

            # read list of column names from INI file. masses are loaded into
            # a list to keep the order. 
            self.config_values['column_names'] = [
                config['column_names'][key] for key in config['column_names']
            ]
            self.config_values['order_columns'] = [
                config['order_columns'][key] for key in config['order_columns']
            ]
            #my_columns = list()
            #for column_name in config['column_names']:
            #    my_columns.append(config['column_names'][column_name])
            
            if self.debug:
                print("Configuration values successfully parsed:")
                for key, value in self.config_values.items():
                    print(f"  {key}: {value}")
       
        except Exception as e:
            sys.exit(f"Error: Could not read configuration file '{self.location}'. Details: {e}")
            
    def get_file_name(self):
        """Returns the name of the input file as specified in the configuration."""
        return self.config_values['file_name']       
    
    def get_round_mz(self)->bool:
        """Returns whether m/z rounding is enabled (True or False)."""
        return self.config_values['round_mz'] 
    
    def get_rounded_column_name(self):
        """Returns the name of the column used for rounded m/z values."""
        return self.config_values['rounded_column_name'] 
          
    def get_mz_column_name(self):
        """Returns the name of the column used for m/z values."""
        return self.config_values['mz_column_name']       
    
    def get_verbose(self):
        """Returns whether verbose mode is enabled (True or False)."""
        return self.config_values['verbose']       
    
    def get_output_file(self):
        """Returns the name of the output file as specified in the configuration."""
        return self.config_values['output_file']       
    
    def get_column_names(self):
        """Returns the list of column names as specified in the configuration."""
        return self.config_values['column_names']       
    
    def get_order_columns(self):
        """Returns the list of ordered columns for display."""
        return self.config_values['order_columns']       
    
if __name__ == "__main__":
    import pprint
    from pathlib import Path
    
    pp = pprint.PrettyPrinter(indent=4)
    
    #import config_file as cfg
    ini_file = Path('./maldi.ini')
    cfg_obj = config_file(location=ini_file, debug=True)
    
    if not os.path.exists(ini_file):
        sys.exit(f"{ini_file} does not exists!.") 

    cfg_obj.read_ini()
    print("Parsed Configuration Values:")
    print(f"  File Name: {cfg_obj.get_file_name()}")
    print(f"  Round m/z: {cfg_obj.get_round_mz()}")
    print(f"  Rounded Column Name: {cfg_obj.get_rounded_column_name()}")
    print(f"  m/z Column Name: {cfg_obj.get_mz_column_name()}")
    print(f"  Verbose: {cfg_obj.get_verbose()}")
    print(f"  Output File: {cfg_obj.get_output_file()}")
    print(f"  Column Names: {cfg_obj.get_column_names()}")
    print(f"  Order Columns: {cfg_obj.get_order_columns()}")
    
    print("\nValidation:")
    value = cfg_obj.get_round_mz()
    print(f"  Round m/z is {'enabled' if value else 'disabled'}")
    
    
    print( "*"*10 )
    ini_file2 = Path('./lcms.ini')
    cfg_obj2 = config_file(location=ini_file2, debug=True)
    
    if not os.path.exists(ini_file2):
        sys.exit(f"{ini_file2} does not exists!.") 

    cfg_obj2.read_ini()
    print(f"file_name={cfg_obj2.get_file_name()}")  
    print(f"round_mz={cfg_obj2.get_round_mz()}")  
    print(f"rounded_column_name={cfg_obj2.get_rounded_column_name()}")  
    print(f"mz_column_name={cfg_obj2.get_mz_column_name()}")  
    print(f"verbose={cfg_obj2.get_verbose()}")  
    print(f"output_file={cfg_obj2.get_output_file()}")  
    print(f"column_names={cfg_obj2.get_column_names()}")  
    print(f"order_columns={cfg_obj2.get_order_columns()}")  
    
    value = cfg_obj2.get_round_mz()
    print (f"object type={type(value)}")
    if value:
        print(f"get_round_mz returns true {value}")
    else:
        print(f"get_round_mz returns False {value}")
