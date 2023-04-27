# import argparse



def main(filename):
    golangLib = load_go_lib('./go/bin/train_result_classifiers.so')

    setup_go_func(golangLib.TrainResultClassifiersGo, [])
    golangLib.TrainResultClassifiersGo()


if __name__ == "__main__":
    main(filename=None)
