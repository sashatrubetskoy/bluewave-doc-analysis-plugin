"""
Compare two pdf files
"""

from goinpy import *
import argparse

VERSION = "1.6.4"


def compare_pdf_files_go(
        filenames,
        methods: list = False,
        pretty_print: bool = False,
        verbose: bool = False,
        regen_cache: bool = False,
        sidecar_only: bool = False,
        no_importance: bool = False,
):
    # library = ctypes.cdll.LoadLibrary('./go/bin/compare_pdfs.so')
    golangLib = load_go_lib('./go/bin/compare_pdfs.so')


    setup_go_func(golangLib.ComparePdfsGo, [
        stringGoSlice,
        stringGoSlice,
        boolGo,
        boolGo,
        boolGo,
        boolGo,
        boolGo,
        boolGo
    ], stringGo)

    # print(filenames[0])
    # stringGo(str_to_go(filenames[0]))
    s1 = list_to_slice([str_to_go(i) for i in filenames], stringGo)
    s2 = list_to_slice([str_to_go(i) for i in methods], stringGo)
    result = golangLib.ComparePdfsGo(
            s1,  # filenames []string,
            s2,  # methods []string,
            boolGo(pretty_print),  # pretty_print bool,
            boolGo(verbose),  # verbose bool,
            boolGo(regen_cache),  # regen_cache bool,
            boolGo(sidecar_only),  # sidecar_only bool,
            boolGo(no_importance),  # no_importance bool,
            boolGo(False),  # aws_config bool,
    )
    print(str_to_py(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--filenames",
        help="PDF filenames to compare",
        nargs="+",
    )
    parser.add_argument(
        "-m",
        "--methods",
        help="Which of the three comparison methods to use: text, digits, images",
        nargs="+",
    )
    parser.add_argument(
        "-p", "--pretty_print", help="Pretty print output", action="store_true"
    )
    parser.add_argument(
        "-c",
        "--regen_cache",
        help="Ignore and overwrite cached data",
        action="store_true",
    )
    parser.add_argument(
        "--sidecar_only",
        help="Just generate sidecar files, dont run analysis",
        action="store_true",
    )
    parser.add_argument(
        "--no_importance", help="Do not generate importance scores", action="store_true"
    )
    parser.add_argument(
        "-v", "--verbose", help="Print things while running", action="store_true"
    )
    parser.add_argument("--version", help="Print version", action="store_true")
    args = parser.parse_args()

    if args.version:
        print(VERSION)
    else:
        compare_pdf_files_go(
            filenames=args.filenames,
            methods=args.methods,
            pretty_print=args.pretty_print,
            verbose=args.verbose,
            regen_cache=args.regen_cache,
            sidecar_only=args.sidecar_only,
            no_importance=args.no_importance,
        )
