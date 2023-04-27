"""
The purpose of this script is to take a bunch of filenames and run the document comparison for all the pairs,
storing the outputs in one big file. This big file will then be  manually labeled for use as training data for
the importance
classifier.
"""

FILENAMES = [
    "/Users/basenko.dv/upwork/bluewave/sample_files/K112226.pdf",
    "/Users/basenko.dv/upwork/bluewave/sample_files/K112422.pdf",
    "/Users/basenko.dv/upwork/bluewave/sample_files/K112844.pdf",
    "/Users/basenko.dv/upwork/bluewave/sample_files/K113500.pdf",
    "/Users/basenko.dv/upwork/bluewave/sample_files/K120084.pdf",
    "/Users/basenko.dv/upwork/bluewave/sample_files/K112376.pdf",
    "/Users/basenko.dv/upwork/bluewave/sample_files/K112205.pdf",
]

from goinpy import *


def main():
    golangLib = load_go_lib('./go/bin/run_and_store_cross_pairs.so')


    setup_go_func(golangLib.RunAndStoreCrossPairsGo, [
        stringGoSlice,
    ], stringGo)

    s1 = list_to_slice([str_to_go(i) for i in FILENAMES], stringGo)

    result = golangLib.RunAndStoreCrossPairsGo(
            s1,  # filenames []string,
    )
    print(str_to_py(result))


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "-f",
    #     "--filenames",
    #     help="PDF filenames to compare",
    #     nargs="+",
    # )
    main()
