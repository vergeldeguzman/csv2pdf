import sys
import argparse
import csv

from lxml import etree

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO


def get_row_column_index(xs, ys, x, y):
    column = None
    if xs and not (x < xs[0]):
        for i in range(1, len(xs)):
            if x < xs[i]:
                column = i - 1
                break;

    row = None
    if ys and not (y < ys[0]):
        for i in range(1, len(ys)):
            if y < ys[i]:
                row = i - 1
                break;
        # adjust row from bottom
        row = len(ys) - row - 2

    return row, column


def parse_xml(xml_data):
    table = []
    try:
        text = {}
        root = etree.XML(xml_data)
        for page_xml in root.iterfind('page[@id]'):
            page_id = page_xml.attrib.get('id')

            xs = []
            ys = []
            for line_xml in page_xml.iterfind('.//line[@bbox]'):
                (x0, y0, x1, y1) = line_xml.attrib.get('bbox').split(',', 4)
                if x0 == x1:
                    xs.append(float(x0))
                if y0 == y1:
                    ys.append(float(y0))

            xs.sort()
            ys.sort()
            r_start = len(table)
            for r in range(len(ys) - 1):
                table.append(['' for c in range(len(xs) - 1)])
            for text_xml in page_xml.iterfind('.//text[@bbox]'):
                (x0, y0, x1, y1) = text_xml.attrib.get('bbox').split(',', 4)
                (r, c) = get_row_column_index(xs, ys, float(x0), float(y0))
                if r is not None and c is not None:
                    table[r_start + r][c] += text_xml.text

    except etree.XMLSyntaxError:
        raise Exception('Cannot parse xml data')

    return table


def write_to_csv(table, csv_file):
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in table:
            writer.writerow(row)


def write_csv_from_pdf(csv_file, pdf_file):
    caching = True
    rsrcmgr = PDFResourceManager(caching=caching)

    pdf_bytes = BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = XMLConverter(rsrcmgr, pdf_bytes, codec=codec, laparams=laparams)

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    max_pages = 0 # all pages
    pagenos=set()

    pdf_fp = open(pdf_file, 'rb')
    for page in PDFPage.get_pages(pdf_fp, pagenos, maxpages=max_pages, password=password,
                                  caching=caching, check_extractable=True):
        interpreter.process_page(page)
    pdf_fp.close()

    device.close()

    pdf_data = pdf_bytes.getvalue()
    pdf_bytes.close()

    table = parse_xml(pdf_data)
    write_to_csv(table, csv_file)


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file',
                        required=True,
                        help='input pdf file')
    parser.add_argument('-o', '--output-file',
                        required=True,
                        help='output csv file')

    args = parser.parse_args()
    return args


def main(argv):
     try:
        args = parse_arg()
        write_csv_from_pdf(args.output_file, args.input_file)
     except Exception as e:
        print(e, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main(sys.argv)
