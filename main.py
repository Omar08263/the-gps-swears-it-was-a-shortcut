"""The GPS Swears It Was a Shortcut — make.fun entry program.

Writes one original line of plain text to /output/entry.txt: the GPS's
own excuse, in its own voice, for sending the driver down the wrong road.

Deterministic: the same bytes on every run. No network, no randomness,
no reads outside this file.
"""

import os
import sys

LINE = "The map swore the lake was a road, and frankly, your car looked thirsty, so I did you both a favor."

EXPECTED_BYTES = 99


def main() -> None:
    data = LINE.encode("utf-8")
    assert len(data) == EXPECTED_BYTES, f"line is {len(data)} bytes, expected {EXPECTED_BYTES}"
    assert 1 <= len(data) <= 200, "line must be 1-200 characters"
    assert data == data.strip(), "line must not be only whitespace"
    # The gate reads one line: a newline anywhere would split the entry.
    assert b"\n" not in data and b"\r" not in data, "line must contain no newline"
    assert data.decode("utf-8").count("\n") == 0, "line must be a single line"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        print(f"read-back mismatch: {written!r} != {data!r}", file=sys.stderr)
        sys.exit(1)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
