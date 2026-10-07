#!/usr/bin/env python3
"""Back up one project file using the file-backup directory and naming rules."""

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path


def name_field(value):
    value = re.sub(r'[\\/:*?"<>|]', "-", value)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise argparse.ArgumentTypeError(
            f"expected lowercase kebab-case, got {value!r}"
        )
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, help="Project root directory")
    parser.add_argument("--backup-dir", required=True, help="Configured backup directory")
    parser.add_argument("--source", required=True, help="Source file within the project")
    parser.add_argument(
        "--description", required=True, type=name_field,
        help="Required lowercase kebab-case description",
    )
    parser.add_argument(
        "--tag", type=name_field, action="append", default=[],
        help="Repeatable lowercase kebab-case tag",
    )
    args = parser.parse_args()

    root = Path(args.project_root).resolve(strict=True)
    source = (root / args.source).resolve(strict=True)
    relative_source = source.relative_to(root)
    backup_dir = (root / args.backup_dir).resolve()

    filename = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename += "--" + args.description
    filename += "".join("+" + tag for tag in args.tag)
    filename += source.suffix
    destination = backup_dir / "files" / relative_source / filename

    with source.open("rb") as original:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as backup:
            shutil.copyfileobj(original, backup)

    print(destination)


if __name__ == "__main__":
    main()
