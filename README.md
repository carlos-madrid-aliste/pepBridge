# pepBridge

Easy way to match MALDI-MSI (m/z) peaks to the peptides (m/z) from LC-MS/MS 


## Features

`pepBridge` is a Python package for processing and matching MALDI and LCMS mass spectrometry data.

- Load MALDI and LCMS data from configuration files and CSVs.
- Match MALDI masses with LCMS masses within a specified tolerance.
- Output matched data to CSV.

`pepBridge` requires two configuration files
## Installation
```bash
pip install pepBridge
from pepBridge import MALDI_LCMS, ConfigFile, MatchingMZ

## Usage

# Display options
python MatchingMZ.py --help
usage: MatchingMZ.py [-h] [--maldi MALDI] [--lcms LCMS] [--mass MASS] [--output OUTPUT]

Easy way to match MALDI-MSI (m/z) peaks to the peptides (m/z) from LC-MS/MS

optional arguments:
  -h, --help       show this help message and exit
  --maldi MALDI    location of the MALDI INI file.
  --lcms LCMS      location of the LCMS INI file.
  --mass MASS      Mass tolerance in Da (default=1.0 Da)
  --output OUTPUT  Output file in CSV format.

# Usage
python MatchingMZ.py --maldi maldi.ini --lcms lcms.ini \ 
             --mass 1.0 --output matched_results_1.0.csv
