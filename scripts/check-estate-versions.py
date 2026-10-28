#!/usr/bin/env python3
"""Check package.json framework pins against estate/versions.json.

estate/versions.json is a copy of the estate framework manifest kept in
roachbait-band/roachbait.band. Every package it lists must carry exactly the
manifest specifier in each dependency field of package.json that declares it.
Packages the manifest names as forbidden must not appear at all. Packages the
manifest does not list may use ranges.

The check prints one ok line and exits zero, or prints each mismatch and exits
non-zero. A built-in self-test runs first and must fail on a seeded drift.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "estate" / "versions.json"
PACKAGE_JSON = ROOT / "package.json"


def mismatches(manifest: dict, package: dict) -> list[str]:
    found: list[str] = []
    pins: dict[str, str] = manifest.get("packages", {})
    forbidden: dict[str, str] = manifest.get("forbidden", {})
    for field in manifest.get("fields", []):
        for name, spec in package.get(field, {}).items():
            if name in forbidden:
                found.append(f"{field}: {name} is forbidden by the manifest")
            elif name in pins and spec != pins[name]:
                found.append(f"{field}: {name} is {spec!r}, the manifest pins {pins[name]!r}")
    return found


def self_test(manifest: dict) -> list[str]:
    pins = manifest.get("packages", {})
    fields = manifest.get("fields", [])
    if not pins or not fields:
        return ["estate/versions.json lists no packages or fields"]
    name = sorted(pins)[0]
    seeded = {fields[0]: {name: "^" + pins[name]}}
    if not mismatches(manifest, seeded):
        return [f"self-test: a ranged {name} specifier did not trip the check"]
    return []


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    package = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    failures = self_test(manifest) + mismatches(manifest, package)
    if failures:
        print("estate version check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print(f"estate versions ok: package.json matches {len(manifest['packages'])} manifest pins")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
