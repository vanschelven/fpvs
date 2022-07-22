import os
import argparse
import yaml
import glob
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from wheel_filename import parse_wheel_filename

from fpvs.__version__ import __version__


def _match(version, affected_ranges):
    for affected_range in affected_ranges.split("||"):
        if Version(version) in SpecifierSet(affected_range):
            return True
    return False


def scan(wheels_path, gemnasium_db_path, verbose=False):
    if verbose:
        print(f"Checking wheels in { wheels_path } against { gemnasium_db_path }")

    for directory in [wheels_path, gemnasium_db_path]:
        if not os.path.isdir(directory):
            print(f"Not a directory: { directory }")
            exit(1)

    failures = {}

    for wheel_filename in glob.glob(f"{ wheels_path }/*.whl"):
        wheel_filename_short = os.path.basename(wheel_filename)
        if verbose:
            print(f"SCANNING { wheel_filename_short }")

        wheel = parse_wheel_filename(wheel_filename)

        for advisory_filename in glob.glob(f"{ gemnasium_db_path }/pypi/{ wheel.project }/*.yml"):
            advisory_filename_short = advisory_filename[len(gemnasium_db_path) + len("/"):]
            with open(advisory_filename, "r") as f:
                advisory = yaml.load(f, yaml.Loader)
                affected_ranges = advisory["affected_range"]
                if affected_ranges == "(,0)":
                    continue

                if verbose:
                    print(
                        f"ADVISORY { advisory_filename_short }: { wheel.version } against { affected_ranges }", end=" ")

                if _match(wheel.version, affected_ranges):
                    if wheel.project not in failures:
                        failures[wheel.project] = wheel.version, []
                    _, advisories = failures[wheel.project]
                    advisories.append(advisory)
                    if verbose:
                        print("FAIL")
                else:
                    if verbose:
                        print("OK")

    if failures and verbose:
        print()  # empty line for readability

    for project, (version, advisories) in failures.items():
        solutions = set()
        print(f"{ project }=={ version }: { len(advisories) } advisories")
        for i, advisory in enumerate(advisories):
            if verbose:
                print()
                print(f"{ i + 1 }. { advisory['title'] }")
                print(f"{ advisory['description'] }")
                print(f"{ advisory['identifier'] }")
            solutions.add(advisory["solution"])

        if verbose:
            print(f"\nSolutions (for { project }=={ version })")

        for solution in sorted(solutions):
            print(solution)

        print()

    if failures:
        print(f"FAILURE: Found { len(failures) } unsafe packages")
        exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wheels-path", help="Directory of wheels to be scanned", default="vendor", type=str)
    parser.add_argument("--gemnasium-db-path", help="Path to gemnasium-db", default="gemnasium-db", type=str)
    parser.add_argument("--version", help="Display version information", action="store_true")
    parser.add_argument("--verbose", default=False, action="store_true")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit()

    scan(args.wheels_path, args.gemnasium_db_path, verbose=args.verbose)
