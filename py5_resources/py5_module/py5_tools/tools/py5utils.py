import argparse

import py5_tools


parser = argparse.ArgumentParser(description="Generate Py5Utilities framework")


def main():
    py5_tools.utilities.generate_utilities_framework()


if __name__ == '__main__':
    main()
