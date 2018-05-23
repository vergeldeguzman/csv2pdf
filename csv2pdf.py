import sys
import argparse
import csv
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A0, A1, A2, A3, A4, A5, A6, B0, B1, B2, B3, B4, B5, B6, letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class PdfWriter():

    def __init__(self, pdf_file, is_landscape, pagesize):
        # Create pdf doc with page size and orientation
        # There is no SimpleDocTemplate.setPageSize API so I have if/else condition on the constructor
        self.doc = SimpleDocTemplate(pdf_file, pagesize=(landscape(pagesize) if is_landscape else pagesize))

        self.data = []

        # Assign grid on all cells (from top left to bottom right)
        self.table_style = [('BOX', (0,0), (-1,-1), 1.5, colors.black),
                            ('INNERGRID', (0,0), (-1,-1), 1, colors.black)]

        self.style = TableStyle(
            [('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 1, colors.black)])

    def enable_header(self):
        # Thick grid on header cells
        self.table_style.append(('BOX', (0,0), (-1,0), 1.5, colors.black))

    def append(self, row):
        self.data.append(row)

    def save(self):
        table=Table(self.data)
        table.hAlign = 'LEFT'
        table.setStyle(self.table_style)
        elements = [table]
        self.doc.build(elements)


def read_csv(csv_file):
    rows = []
    with open(csv_file, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    return rows


def write_pdf_from_csv(pdf_file, csv_file, has_header, is_landscape, pagesize):

    pdf_writer = PdfWriter(pdf_file, is_landscape, pagesize)
    if has_header:
        pdf_writer.enable_header()

    rows = read_csv(csv_file)
    for row in rows:
        pdf_writer.append(row)

    pdf_writer.save()


def translate_pagesize(arg_pagesize):
    if arg_pagesize == 'letter':
        return letter

    a_pagesizes = [A0,A1,A2,A3,A4,A5,A6]
    b_pagesizes = [B0,B1,B2,B3,B4,B5,B6]

    m = re.match('^A([0-6])$', arg_pagesize)
    if m:
        return a_pagesizes[int(m.group(1))]

    m = re.match('B([0-6])$', arg_pagesize)
    if m:
        return b_pagesizes[int(m.group(1))]

    raise('Unrecognize pagesize: ' + arg_pagesize)


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file',
                        required=True,
                        help='input csv file')
    parser.add_argument('-o', '--output-file',
                        required=True,
                        help='output pdf file')
    parser.add_argument('-c', '--contain-header',
                        action='store_true',
                        help='table contains header (first row)')
    parser.add_argument('-l', '--landscape',
                        action='store_true',
                        help='landscape page')
    parser.add_argument('-p', '--pagesize',
                        default='letter',
                        choices=['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6',
                                 'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6',
                                 'letter'],
                        metavar='PAGESIZE',
                        help='pagesize, valid choices are: A0,A1,A2,A3,A4,A5,A6,B0,B1,B2,B3,B4,B5,B6,letter')

    args = parser.parse_args()
    return args


def main(argv):
    try:
        args = parse_arg()
        write_pdf_from_csv(args.output_file, args.input_file, args.contain_header, args.landscape,
                           translate_pagesize(args.pagesize))
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main(sys.argv)

