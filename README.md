# pepBridge

Easy way to match MALDI-MSI (m/z) peaks to the peptides (m/z) from LC-MS/MS 


## Features

`pepBridge` is a Python package for processing and matching MALDI and LCMS mass spectrometry data.

- Load MALDI and LCMS data from configuration files and CSVs.
- Match MALDI masses with LCMS masses within a specified tolerance.
- Output matched data to CSV.



## Installation

The easiest way to work with pepBridge is by using Anaconda and configuring a virtual environment. Anaconda 
is a Python distribution plus a packaging manager called conda.

### a. Create and configure a virtual environment

```bash
conda create --name pepBridge python=3.9
```

### c. Activate the new virtual environment
```bash
conda activate pepBridge
```

### d. Install pepBridge package
```bash
pip install -i https://test.pypi.org/simple/ pepBridge

```

## Usage

```bash
python pepbridge --help
usage: pepbridge [-h] [--maldi MALDI] [--lcms LCMS] [--mass MASS] [--output OUTPUT]

Easy way to match MALDI-MSI (m/z) peaks to the peptides (m/z) from LC-MS/MS

optional arguments:
  -h, --help       show this help message and exit
  --maldi MALDI    location of the MALDI INI file.
  --lcms LCMS      location of the LCMS INI file.
  --mass MASS      Mass tolerance in Da (default=1.0 Da)
  --output OUTPUT  Output file in CSV format.
```

## Running pepbridge
```bash
python pepbridge  --maldi maldi.ini --lcms lcms.ini --mass 1.0 --output matched_results_1.0.csv
```


`pepBridge` requires two configuration files
```bash 
## maldi.ini file

[file]
; Specify the full file path of the MALDI CSV file that contains your data.
; This file is used as input for comparison with LCMS data.
name=/home/cmadrid/DATA/199-196/4K/IMS199_OTD196_GK_Thymus_ChemoL_v_CtrlR_MALDI_Match_LCMS_4K_MALDI.csv

[round_mz]
; Determine whether the m/z values should be rounded to the nearest integer 
; before comparing them with LCMS data. Set to "True" to round m/z value
value=True
column_name=rounded_mz

[mz_column_name]
; Specify the name of the column that hold the m/z values in the CSV file.
name=${column_names:column1}

[verbose]
; Enable or disable verbose output during the process.
; Set to "True" for detailed logs to help with troubleshooting or understanding the process.
value=True


[column_names]
; Define the names of the columns in the MALDI CSV file. These column names will be used for data extraction.
column1=m/z
column2=Average
column3=IMS199_Chemo_Left_4K
column4=IMS199_Control_Right_Bottom_4K
column5=IMS199_Control_Right_Top_4K

[order_columns]
; Specify the order in which columns should appear in the output file.
; The columns will be printed in the specified order, with optional modifications such as rounded m/z.
column1=${column_names:column1}
column2=${round_mz:column_name}
column3=${column_names:column2}
column4=${column_names:column3}
column5=${column_names:column4}
column6=${column_names:column5}
```

## lcms.ini file
```bash
[file]
; specify the location of the LCMS csv file
name=/home/cmadrid/DATA/withTrypsin/IMS199_OTD196_GK_Thymus_ChemoL_v_CtrlR_MALDI_Match_LCMS_wTrypsinR05_4K_Oct2024_LCMS.csv

; specify if m/z should be rounded to the nearest integer before performing 
; the m/z comparison. 
[round_mz]
value=True
column_name=rounded_mz

[mz_column_name]
name=${column_names:column1}

[verbose]
value=True


[column_names]
column1=Theo. MH+ [Da]
column2=Master Protein Accessions
column3=Master Protein Descriptions
column4=Gene Name
column5=Annotated Sequence
column6=Modifications
column7=196a_Left_1 Chemo
column8=196a_Right_2 - Control
column9=log2 ratio Chemo vs Control

[order_columns]
column1=${column_names:column1}
column2=${round_mz:column_name}
column3=${column_names:column2}
column4=${column_names:column3}
column5=${column_names:column4}
column6=${column_names:column5}
column7=${column_names:column6}
column8=${column_names:column7}
column9=${column_names:column8}
column10=${column_names:column9}
```
