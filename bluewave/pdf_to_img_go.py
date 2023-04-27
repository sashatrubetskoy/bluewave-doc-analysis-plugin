"""
Example usages:

    python py/pdf_to_img.py -f data/test_pdfs/00026_04_fda-K071597_test_data.pdf -p 4 -o .

    python py/pdf_to_img.py -f data/test_pdfs/00026_04_fda-K071597_test_data.pdf -p 4-9 -o tmp

    python py/pdf_to_img.py -f data/test_pdfs/00026_04_fda-K071597_test_data.pdf -p 1,2,4-9 -o tmp

Pages can be specified 1,2,3 and/or 10-20. The out directory must exist
beforehand (e.g. mkdir tmp)

Note that, for page input, pages start with 1 (not zero)
"""

import argparse
from goinpy import *


def pdf_to_image(filename: str, pages: str, outpath: str):
    golangLib = load_go_lib('./go/bin/pdf_to_img.so')
    setup_go_func(golangLib.PdfToImgGo, [
        stringGo,
        stringGo,
        stringGo,
    ], stringGo)

    result = golangLib.PdfToImgGo(
        str_to_go(filename),  # filenames []string,
        str_to_go(pages),  # methods []string,
        str_to_go(outpath),  # methods []string,
    )
    print(str_to_py(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--filename",
        help="PDF filename to create thumbnails of",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--pages",
        help='Pages to create thumbnails of (e.g. "1,2,3" or "3,5-10")',
        required=True,
    )
    parser.add_argument(
        "-o",
        "--outpath",
        help="path where to save resulting images",
        required=True,
    )
    args = parser.parse_args()

    pdf_to_image(filename=args.filename, pages=args.pages, outpath=args.outpath)
