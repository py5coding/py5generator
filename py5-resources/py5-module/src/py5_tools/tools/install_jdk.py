# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2026 Jim Schmitz
#
#   This library is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 2.1 of the License, or (at
#   your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
#   General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this library. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
import argparse
import sys

parser = argparse.ArgumentParser(description="Install Java Development Environment")
parser.add_argument(
    "-j",
    "--java-version",
    action="store",
    dest="java_version",
    default=21,
    type=int,
    help="Java Version (must be 17 or greater, defaults to 21)",
)


def main():
    args = parser.parse_args()

    try:
        import jdk
    except ImportError:
        print(
            "Please first install the python library `install-jdk` using the command `pip install install-jdk`",
            file=sys.stderr,
        )
        return

    java_version = args.java_version

    if java_version < 17:
        print(
            f"Java version must be 17 or greater, please specify a different version using the -j option"
        )
        return

    try:
        print(f"Installing Java Development Environment version {java_version}...")
        print(f"Java installed to {jdk.install(java_version)}")
    except jdk.JdkError as e:
        print(f"Failed to install Java: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
