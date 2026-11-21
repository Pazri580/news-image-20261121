#!/usr/bin/env python3
"""Publish this entry's front page image.

The repository already carries the finished picture as ``entry.png``
(next to this file). This script copies that file into the output
directory the grader points at, then reads the copy back and checks
that its SHA-256 digest still matches the original, so a truncated or
altered write is caught instead of silently submitted.

Only the Python standard library is used. No network access, no
external programs, no image libraries: the picture is moved as raw
bytes, which keeps the output byte-for-byte identical to the source.
"""

import hashlib
import os
import sys

# The picture that ships with this repository.
SOURCE_NAME = "entry.png"

# Where the grader expects the finished picture. The environment
# variable wins when it is set; otherwise the default output path
# is used.
OUTPUT_ENV = "MAKEFUN_OUTPUT_DIR"
OUTPUT_DEFAULT = "/output"


def digest_of(data):
    """Return the hex SHA-256 digest of a bytes object."""
    return hashlib.sha256(data).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, SOURCE_NAME)

    with open(source_path, "rb") as handle:
        picture = handle.read()
    source_digest = digest_of(picture)

    output_dir = os.environ.get(OUTPUT_ENV, OUTPUT_DEFAULT)
    os.makedirs(output_dir, exist_ok=True)
    target_path = os.path.join(output_dir, SOURCE_NAME)

    with open(target_path, "wb") as handle:
        handle.write(picture)

    with open(target_path, "rb") as handle:
        written = handle.read()
    written_digest = digest_of(written)

    if written_digest != source_digest:
        print(
            "ERROR: sha256 mismatch after writing %s "
            "(source %s, written %s)" % (target_path, source_digest, written_digest),
            file=sys.stderr,
        )
        return 1

    print(
        "wrote %s (%d bytes, sha256 %s)"
        % (target_path, len(written), written_digest)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
