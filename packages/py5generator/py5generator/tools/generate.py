import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Generate py5 library using processing jars",
                                 epilog="this is the epilog")


parser.add_argument(action='store', dest='py5_destination_dir', default='.',
                    help='location to write generated py5 library')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-r', '--repo', action='store', dest='processing_repo_dir',
                   help='location of processing code (github repository)')
group.add_argument('-p', '--pde', action='store', dest='processing_install_dir',
                   help='location of installed processing application (PDE)')


def generate(dest_dir, repo_dir=None, install_dir=None):
    from py5generator import generator  # noqa
    dest_dir = Path(dest_dir)
    repo_dir = repo_dir and Path(repo_dir)
    install_dir = install_dir and Path(install_dir)
    generator.generate_py5(dest_dir, repo_dir=repo_dir, install_dir=install_dir)


def main():
    args = parser.parse_args()
    generate(args.py5_destination_dir,
             repo_dir=args.processing_repo_dir,
             install_dir=args.processing_install_dir)


if __name__ == '__main__':
    main()
