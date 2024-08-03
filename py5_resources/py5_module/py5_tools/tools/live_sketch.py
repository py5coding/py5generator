# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2024 Jim Schmitz
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

from py5_tools import live_coding

parser = argparse.ArgumentParser(description="Live coding for module mode py5 sketches")
parser.add_argument(action="store", dest="sketch_path", help="path to py5 sketch")
parser.add_argument(
    "--always-rerun-setup",
    action=argparse.BooleanOptionalAction,
    default=False,
    dest="always_rerun_setup",
    help="always rerun setup function when file is updated",
)
parser.add_argument(
    "--always-on-top",
    action=argparse.BooleanOptionalAction,
    default=True,
    dest="always_on_top",
    help="keep sketch on top of other windows",
)
parser.add_argument(
    "-s",
    "--screenshot-dir",
    action="store",
    dest="screenshot_dir",
    help="directory to save screenshots",
)
parser.add_argument(
    "-b",
    "--code-backup-dir",
    action="store",
    dest="code_backup_dir",
    help="directory to save code backups",
)


def main():
    args = parser.parse_args()
    live_coding.launch_live_coding(
        args.sketch_path,
        always_rerun_setup=args.always_rerun_setup,
        always_on_top=args.always_on_top,
        screenshot_dir=args.screenshot_dir,
        code_backup_dir=args.code_backup_dir,
    )


if __name__ == "__main__":
    main()
