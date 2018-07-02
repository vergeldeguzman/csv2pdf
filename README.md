# csv2pdf / pdf2csv

csv2pdf - convert csv to pdf

pdf2csv - convert pdf to csv, can only converts table with inner grid and outer grid 

## Usage

```
usage: csv2pdf.py [-h] -i INPUT_FILE -o OUTPUT_FILE [-c] [-l] [-p PAGESIZE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        input csv file
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        output pdf file
  -c, --contain-header  table contains header (first row)
  -l, --landscape       landscape page
  -p PAGESIZE, --pagesize PAGESIZE
                        pagesize, valid choices are:
                        A0,A1,A2,A3,A4,A5,A6,B0,B1,B2,B3,B4,B5,B6,letter
```

```  
usage: pdf2csv.py [-h] -i INPUT_FILE -o OUTPUT_FILE

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        input pdf file
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        output csv file  
  ```
  
## Requirements

    python 3.5
    lxml
    reportlab
    dataminer.six

## Example run

Convert csv file to pdf file (default to letter page)

```
python.exe csv2pdf.py -i input.csv -o output.pdf
```

Convert csv file with header row to pdf file (landscape A4)

```
python.exe csv2pdf.py -i input.csv -o output.pdf -c -l -p A4
```

Convert pdf file to csv file

```
python.exe pdf2csv.py -i input.pdf -o output.csv
```
