import argparse

import py5_tools


parser = argparse.ArgumentParser(description="Generate Py5Utilities framework")
parser.add_argument('-d', '--destination', action='store', dest='destination',
                    help='output destination if not current directory')


def main():
    args = parser.parse_args()
    py5_tools.utilities.generate_utilities_framework(args.destination)


if __name__ == '__main__':
    main()
