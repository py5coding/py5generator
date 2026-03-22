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

parser = argparse.ArgumentParser(description="Install Java Development Kit")
parser.add_argument(
    "-j",
    "--java-version",
    action="store",
    dest="java_version",
    default=21,
    type=int,
    help="Java Version (must be 17 or greater, defaults to 21)",
)
parser.add_argument(
    "--jre",
    action="store_true",
    dest="jre",
    default=False,
    help="Install Java Runtime Environment (JRE) instead of Java Development Kit (JDK)",
)


def main(args=None):
    args = args or parser.parse_args()

    try:
        import jdk
    except ImportError:
        print(
            "Please first install the python library `install-jdk` using the command `pip install install-jdk`",
            file=sys.stderr,
        )
        return

    java_version = args.java_version
    jre = args.jre

    installing = "Java Runtime Environment" if jre else "Java Development Kit"

    if java_version < 17:
        print(
            f"Java version must be 17 or greater, please specify a different version using the -j option"
        )
        return

    try:
        print(f"Installing {installing} version {java_version}...")
        print(
            f"{installing} version {java_version} installed to {jdk.install(java_version, jre=jre)}"
        )
    except jdk.JdkError as e:
        print(
            f"Failed to install {installing} version {java_version}: {e}",
            file=sys.stderr,
        )
        print(
            "Make sure you have a working internet and that have not installed this version of Java already.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
