# csv2pdf

csv2pdf is a script that converts csv to pdf. 

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
  
## Requirements

    python 3.5
    reportlab

## Example run

Convert csv file to pdf file (default to letter page)

```
python.exe csv2pdf.py -i input.csv -o output.pdf
```

Convert csv file with header row to pdf file (landscape A4)

```
python.exe csv2pdf.py -i input.csv -o output.pdf -c -l -p A4
```
