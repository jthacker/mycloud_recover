import argparse
import os

from mycloud_recover.recover import recover

parser = argparse.ArgumentParser(prog="mycloud_recover")
parser.add_argument(
    "--verbose",
    action="store_true",
    help="Print detailed information about the recovery",
)
parser.add_argument("--no-write", action="store_true", help="Do not write anything")
parser.add_argument("input", help="Path to restsdk input directory")
parser.add_argument("output", help="Path to output directory where files are written")


def main(args=None):
    if args is None:
        args = parser.parse_args()

    db_path = os.path.join(args.input, "data/db/index.db")
    if not os.path.exists(db_path):
        raise ValueError(
            f"Error finding db in input path {args.input!r}, tried {db_path!r}"
        )
    content_dir = os.path.join(args.input, "data/files")
    if not os.path.exists(content_dir):
        raise ValueError(
            f"Error finding content directory in input path {args.input!r}, tried {content_dir!r}"
        )
    if not os.path.exists(args.output):
        raise ValueError(f"Error finding output directory {args.output!r}")

    recover(
        db_path=db_path,
        content_dir=content_dir,
        output_dir=args.output,
        verbose=args.verbose,
        no_write=args.no_write,
    )
