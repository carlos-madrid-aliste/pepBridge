import numpy as np
import csv
import sys
import pprint
import argparse
import os
import MALDI_LCMS as m

class MatchingMZ:
    """
    A class to match MALDI data with LCMS data based on m/z values.

    This class loads MALDI and LCMS data, performs matching of m/z values
    within a specified tolerance (delta), and outputs the matches.
    """
    def __init__(self, maldi_ini_file, lcms_ini_file, debug=False) -> None:
        """
        Initialize the MatchingMZ object.

        Args:
            maldi_ini_file (str): Path to the MALDI INI configuration file.
            lcms_ini_file (str): Path to the LCMS INI configuration file.
            debug (bool): Enable debugging messages if True.
        """
        
        self.maldi_ini_file = maldi_ini_file
        self.lcms_ini_file  = lcms_ini_file
        self.debug = debug
        
        # Initialize MALDI and LCSM objects
        self.maldi_obj = m.MALDI_LCMS(config_file=maldi_ini_file, debug=self.debug) 
        self.lcms_obj  = m.MALDI_LCMS(config_file=lcms_ini_file, debug=self.debug) 
        
    def get_hits(self, maldi_mass, np_lcms_masses, np_lcms_file, delta=0):
        """
        Extract all rows from the LCMS data where the m/z value matches a MALDI mass within a given delta.

        Args:
            maldi_mass (float): The m/z value from the MALDI dataset.
            np_lcms_masses (np.ndarray): Array of m/z values from the LCMS dataset.
            np_lcms_file (np.ndarray): Array representing the LCMS dataset (str array).
            delta (float): Tolerance for matching m/z values (default: 0 Da).

        Returns:
            np.ndarray or None: Rows from the LCMS dataset that match the MALDI mass.
        """
        # Calculate the absolute difference and find matches within the delta
        matches = np.abs(np_lcms_masses - maldi_mass) <= delta
        #matches = (np.abs(np_lcms_masses - maldi_mass) ) 
        #matches = matches <= delta
        
        if np.any(matches):
            return np_lcms_file[matches]
        return None

    def write(self, data_file, output_file):
        """
        Write the matched MALDI and LCMS data to a CSV file.

        Args:
            data_file (list): List of matched data rows.
            output_file (str): Path to the output CSV file.
        """
        maldi_headers = self.maldi_obj.get_ordered_columns()
        lcms_headers  = self.lcms_obj.get_ordered_columns()
        headers = maldi_headers + lcms_headers
        
        if self.debug:
            print(f"Headers: {headers}")
            print(f"Sample data (first 2 rows): {data_file[:2]}")
        
        with open(output_file, mode='w', newline='') as csv_file:
            dwriter = csv.writer(csv_file, dialect='excel')
            dwriter.writerow(headers)    # write headers
            dwriter.writerows(data_file) # write data rows
        
        if self.debug:
            print(f"Data written to {output_file}")    

    def match_maldi_in_lcms(self, delta=0):
        """
        Match MALDI m/z values with LCMS m/z values within a specified delta.

        Args:
            delta (float): Tolerance for matching m/z values (default: 0).

        Returns:
            list: A list of matched data rows.
        """
        # load MALDI and LCMS datasets
        self.maldi_obj.load()
        maldi_file = self.maldi_obj.get_file() 
        
        self.lcms_obj.load() 
        lcms_file = self.lcms_obj.get_file()
        # get_file method returns the LCMS of MALDI file in the order
        # specified in the [order_columns] section.
        
        #  Extract m/z values from both datasets
        lcms_masses  = self.lcms_obj.extract_mz()
        maldi_masses = self.maldi_obj.extract_mz()

        # Convert lists to NumPy arrays for efficient processing
        np_maldi_file  = np.array(maldi_file[1:], dtype=np.float64)
        np_lcms_file   = np.array(lcms_file,  dtype=str)
        np_lcms_masses = np.array(lcms_masses,  dtype=np.float64)  
        np_maldi_masses= np.array(maldi_masses, dtype=np.float64)  
        
        if self.debug:
            print("NumPy conversion completed.")
            print(f"MALDI File: {np_maldi_file.shape}")
            print(f"LCMS File: {np_lcms_file.shape}")
        
        #for maldi_mass in np_maldi_masses:
        matched_rows = list()
        for line in np_maldi_file:
            # keep in mind that line is a "list" containing the lines of the maldi file.            
            # That maldi_file was stored in memory according to the order specified 
            # in [order_columns] INI section. 

            # From the MALDI file get the m/z that we want to compare
            # it could the rounded_mz or non-rounded
            maldi_mass_index = self.maldi_obj.locate_mz()
            maldi_mass = line[maldi_mass_index]
            
            # Find matching rows in LCMS
            hits = self.get_hits(maldi_mass, np_lcms_masses, np_lcms_file, delta)
            if hits is None:
                print(f"No matches for MALDI mass: {maldi_mass}")
            else:
                #print(f"maldi_mass = {maldi_mass} hits={len(hits)}")
                print(f"{len(hits)} matches found for MALDI mass: {maldi_mass}")
                # Combine MALDI and LCMS rows for output
                # concatenate the line from MALDI with the hits of LCMS lines.
                # Using loops for numpy array operations is less efficient
                # than using vectorized operations, but this is the only way 
                # that I figure out to do the concatenation.
                for lcms_row in hits:
                    matched_rows.append(np.concatenate((line, lcms_row)).tolist())    
        return matched_rows             
    
def read_options(args=sys.argv[1:]):

    # construct the argument parser
    parser = argparse.ArgumentParser(
        description="Easy way to match MALDI-MSI (m/z) peaks to the peptides (m/z) from LC-MS/MS",
        epilog='Written by Carlos Madrid-Aliste.'
    )
    
    # add the positional arguments to the Argument Parser
    parser.add_argument("--maldi", default='maldi.ini', help="location of the MALDI INI file.")
    parser.add_argument("--lcms",  default='lcms.ini', help="location of the LCMS INI file.")
    parser.add_argument("--mass",  default='1.0', help="Mass tolerance in Da (default=1.0 Da)")
    parser.add_argument("--output",default='matched_results_1.0.csv', help="Output file in CSV format.")
        
    # parse arguments from terminal
    opts = parser.parse_args(args)
    
    # manually catching mistakes
    if not opts.maldi:  
        parser.error("MALDI INI file is required\nPlease type pepBridge --help")
    if not opts.lcms:   
        parser.error("LCMS INI file is required\nPlease type pepBridge --help")

    return opts
        
if __name__ == "__main__":
    
    # call the function to read the argument values
    opts = read_options(sys.argv[1:])
    m_file = opts.maldi
    l_file = opts.lcms
    delta = float(opts.mass)       # Mass tolerance in Daltons
    output_filename = opts.output  # Name of the output file
    #output_filename = f"matched_results_{delta}.csv"
    
    if not os.path.exists(m_file):
        sys.exit(f"{m_file} does not exists in current directory.\n")
    if not os.path.exists(l_file):
        sys.exit(f"{l_file} does not exists in current directory.\n")
        
    # Initialize the MatchingMZ object
    matcher = MatchingMZ(maldi_ini_file=m_file, lcms_ini_file=l_file, debug=False)
    
    # Perform the matching
    matches = matcher.match_maldi_in_lcms(delta=delta)
    
    # Write the results to a CSV file
    matcher.write(matches, output_filename)
    