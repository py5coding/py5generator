import argparse

import py5_tools


parser = argparse.ArgumentParser(description="Generate Py5Utilities framework")
parser.add_argument('-o', '--output', action='store', dest='output_dir',
                    help='output destination (defaults to current directory)')
parser.add_argument('-j', '--jars', action='store', dest='jars_dir',
                    help='jar directory (defaults to jars subdirectory)')


def main():
    args = parser.parse_args()
    py5_tools.utilities.generate_utilities_framework(args.output_dir, args.jars_dir)


if __name__ == '__main__':
    main()
