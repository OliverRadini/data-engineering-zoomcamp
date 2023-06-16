import argparse


def parse_standard_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--color")
    parser.add_argument("--year")
    parser.add_argument("--month")

    return parser.parse_args()
