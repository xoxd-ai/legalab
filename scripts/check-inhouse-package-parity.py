#!/usr/bin/env python3
"""Assert Bazel-only ingestion of the in-house @tummycrypt, @tinyland and @xoxd packages.

Copied from xoxd-ai/site.scaffold scripts/check-inhouse-package-parity.py at
3d4db5e. This copy adds the @xoxd scope, because the Legalab site links the
shared xoxd chrome and theme modules.

TIN-2838 flipped the scaffold from an npm-shadow ingestion (org packages listed
as npm specifiers in package.json, versions kept in exact parity with the
bazel_dep pins) to Bazel-only ingestion: the org packages are graph-linked from
tinyland-inc/bazel-registry via `npm_link_package` and carry NO npm specifier at
all. The pnpm/npm path can no longer supply them.

The invariant this check enforces (conformance item 13):

  1. NO @tummycrypt/* or @tinyland/* npm specifier may remain in package.json
     (any of dependencies / devDependencies / peerDependencies /
     optionalDependencies). Any lingering specifier is npm-shadow ingestion and
     is forbidden.
  2. Every org package the repo graph-links MUST be present as BOTH a
     `bazel_dep(...)` in MODULE.bazel AND an `npm_link_package(...)` entry in
     BUILD.bazel (the two halves of a Bazel-only ingestion edge).

resolution-layer extension (2026-08-31): (1) and (2) above only prove the
*declaration* layer -- MODULE.bazel names the right module and version, and
BUILD.bazel links it. Neither ever opens MODULE.bazel.lock, so a lock whose
registryFileHashes point an in-house module at npmjs.org, or a missing lock
entirely, both passed silently before this extension -- proved by mutating a
copy of the real lock and confirming the prior version of this script stayed
green. The functions below close that: they require every in-house
bazel_dep's MODULE.bazel + source.json to be recorded in the lock under the
exact registry URL pinned in .bazelrc's `common --registry=` line, and they
self-test that requirement by mutating a parsed copy of the lock in memory
before trusting it against the real file. Paired with `common
--lockfile_mode=error` in .bazelrc, which makes Bazel itself refuse to
silently regenerate a drifted lock.

LIMITS, stated plainly -- what a green run here does NOT mean: it does not
mean the site consumes an in-house package's BYTES through Bazel at build
time; that is invariant (2) above (bazel_dep + npm_link_package). The
resolution-layer functions only prove provenance of the MODULE GRAPH's
metadata -- each in-house module's MODULE.bazel + source.json came from the
pinned registry commit, not some other host -- nothing about the shipped
package contents themselves.

Every check above depends on parse_bazel_deps(), which reads MODULE.bazel's
`bazel_dep(...)` calls kwarg-order-agnostically. That matters for safety, not
tidiness: a parser that requires `version` to sit immediately after `name`
silently drops `bazel_dep(name = "x", dev_dependency = True, version = "1.0")`,
and a dropped in-house dep is fail-OPEN here because it escapes the
resolution-layer audit entirely instead of tripping it. parser_self_test()
asserts the order-independence before any real check runs.

The report style matches the prior parity check: failures print to stderr as
`  - <detail>` bullets and the script exits non-zero; a clean run prints a
one-line ok summary and exits zero.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_JSON = ROOT / "package.json"
MODULE_BAZEL = ROOT / "MODULE.bazel"
BUILD_BAZEL = ROOT / "BUILD.bazel"
MODULE_BAZEL_LOCK = ROOT / "MODULE.bazel.lock"
BAZELRC = ROOT / ".bazelrc"
IN_HOUSE_SCOPES = ("@tummycrypt/", "@tinyland/", "@xoxd/")
# Must stay in sync with IN_HOUSE_SCOPES: npm_to_bazel_module() lowercases the
# scope, strips the "@", and appends "_" as the module-name separator.
IN_HOUSE_MODULE_PREFIXES = ("tummycrypt_", "tinyland_", "xoxd_")

# The pinned bazel-registry line this repo's .bazelrc carries (xoxd-ai, the
# canonical owner, or the legacy tinyland-inc spelling),
# e.g. "common --registry=https://raw.githubusercontent.com/xoxd-ai/
# bazel-registry/<40-hex-sha>". Captures the base URL (used to build expected
# lock keys) and the bare SHA (used only in failure messages).
REGISTRY_PIN_RE = re.compile(
    r"^common --registry=(?P<url>https://raw\.githubusercontent\.com/"
    r"(?:xoxd-ai|tinyland-inc)/bazel-registry/(?P<sha>[0-9a-f]{40}))\s*$",
    re.MULTILINE,
)

# Artifacts the Bzlmod resolver must have fetched, and hashed into the lock,
# for every in-house module: the module manifest and its source pin.
RESOLUTION_ARTIFACTS = ("MODULE.bazel", "source.json")


def npm_to_bazel_module(package_name: str) -> str:
    scope, name = package_name.split("/", 1)
    return f"{scope[1:]}_{name}".replace("-", "_")


def load_inhouse_npm_specifiers() -> dict[str, str]:
    """Any @tummycrypt/@tinyland specifier still declared as an npm dependency."""
    package = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    specifiers: dict[str, str] = {}
    for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        for name, version in package.get(section, {}).items():
            if name.startswith(IN_HOUSE_SCOPES):
                specifiers[name] = str(version)
    return specifiers


def load_graph_linked_packages() -> set[str]:
    """npm package names graph-linked via npm_link_package in BUILD.bazel."""
    text = BUILD_BAZEL.read_text(encoding="utf-8")
    linked: set[str] = set()
    for match in re.finditer(
        r'npm_link_package\(\s*name\s*=\s*"node_modules/(@[^"]+)"',
        text,
        flags=re.MULTILINE,
    ):
        package_name = match.group(1)
        if package_name.startswith(IN_HOUSE_SCOPES):
            linked.add(package_name)
    return linked


def parse_bazel_deps(text: str) -> dict[str, str]:
    """Parse `bazel_dep(...)` calls out of MODULE.bazel text, keyed by module
    name, valued by version ("" when the call declares no version=).

    Deliberately kwarg-ORDER-AGNOSTIC. A single regex requiring `version` to
    sit immediately after `name` silently drops any dep written as e.g.
    `bazel_dep(name = "x", dev_dependency = True, version = "1.0")` -- both
    legal Starlark and common in the wild. Dropping a dep here is fail-OPEN
    for the resolution-layer check (an unaudited in-house module), so each
    call's argument list is scanned for `name` and `version` independently.
    bazel_dep argument lists contain no nested parentheses, so matching to the
    first `)` is enough.
    """
    deps: dict[str, str] = {}
    for call in re.finditer(r"bazel_dep\(([^)]*)\)", text, flags=re.DOTALL):
        args = call.group(1)
        name_match = re.search(r'\bname\s*=\s*"([^"]+)"', args)
        if name_match is None:
            continue
        version_match = re.search(r'\bversion\s*=\s*"([^"]*)"', args)
        deps[name_match.group(1)] = version_match.group(1) if version_match else ""
    return deps


def load_bazel_deps() -> dict[str, str]:
    """Every bazel_dep in MODULE.bazel, keyed by module name, valued by version."""
    return parse_bazel_deps(MODULE_BAZEL.read_text(encoding="utf-8"))


def inhouse_bazel_deps(bazel_deps: dict[str, str]) -> dict[str, str]:
    """All in-house modules declared in MODULE.bazel, keyed by module name.

    Unlike load_graph_linked_packages(), this is not filtered by BUILD.bazel
    npm_link_package entries: it covers every in-house bazel_dep regardless of
    whether it is graph-linked yet, so the resolution-layer check still audits
    a module that is declared but not (or not yet) linked.
    """
    return {
        name: version
        for name, version in bazel_deps.items()
        if name.startswith(IN_HOUSE_MODULE_PREFIXES)
    }


def load_pinned_registry() -> tuple[str, str] | None:
    """Return (pinned base URL, pinned SHA) from .bazelrc's registry line."""
    text = BAZELRC.read_text(encoding="utf-8")
    match = REGISTRY_PIN_RE.search(text)
    if match is None:
        return None
    return match.group("url"), match.group("sha")


def resolution_layer_failures(
    inhouse_deps: dict[str, str],
    pinned: tuple[str, str] | None,
    hashes: dict[str, object] | None,
    *,
    lock_present: bool,
) -> list[str]:
    """Prove every in-house bazel_dep resolves from the pinned registry SHA at
    the Bzlmod *resolution* layer (MODULE.bazel.lock's registryFileHashes),
    not merely the declaration layer (MODULE.bazel). Pure function over
    already-parsed inputs so the self-test below can mutate them in memory
    without touching the real lock file.

    Fails closed: no in-house deps to check is reported as its own failure by
    the caller (callers should not treat "nothing to check" as success), a
    missing or empty lock fails, and any in-house artifact resolved from a URL
    other than the pinned one fails, whether that URL is a stray registry
    commit or an entirely different host (npmjs.org, bcr.bazel.build, etc.).
    """
    failures: list[str] = []

    if pinned is None:
        failures.append(
            ".bazelrc has no pinned xoxd-ai/bazel-registry "
            "'common --registry=https://raw.githubusercontent.com/xoxd-ai/"
            "bazel-registry/<sha>' line to check the lock against"
        )
        return failures
    pinned_url, pinned_sha = pinned

    if not lock_present:
        failures.append(
            "MODULE.bazel.lock is missing; cannot prove in-house modules "
            "resolve from the pinned bazel-registry commit rather than npm "
            "or an unpinned registry"
        )
        return failures

    if not hashes:
        failures.append(
            "MODULE.bazel.lock has no registryFileHashes entries; the "
            "resolution layer cannot be audited"
        )
        return failures

    for module_name, version in sorted(inhouse_deps.items()):
        if not version:
            failures.append(
                f"{module_name} is declared as a bazel_dep with no version= in "
                "MODULE.bazel; its resolution cannot be audited against the "
                "pinned registry"
            )
            continue
        for artifact in RESOLUTION_ARTIFACTS:
            expected_key = f"{pinned_url}/modules/{module_name}/{version}/{artifact}"
            if expected_key in hashes:
                continue
            suffix = f"/modules/{module_name}/{version}/{artifact}"
            stray_keys = sorted(key for key in hashes if key.endswith(suffix))
            if stray_keys:
                failures.append(
                    f"{module_name}@{version} {artifact} resolves from "
                    f"{stray_keys[0]!r}, not the pinned registry commit {pinned_sha}"
                )
            else:
                failures.append(
                    f"{module_name}@{version} {artifact} has no "
                    "registryFileHashes entry under the pinned registry at all"
                )

    return failures


def resolution_layer_self_test(
    inhouse_deps: dict[str, str],
    pinned: tuple[str, str] | None,
    hashes: dict[str, object] | None,
) -> list[str]:
    """Negative controls: mutate a parsed copy of the real lock in memory and
    assert resolution_layer_failures() actually trips on each mutation. If a
    mutation stays green, the check above is not discriminating and this
    reports that as a failure in its own right, matching the house pattern of
    self-testing a gate rather than trusting it by inspection alone.
    """
    self_test_failures: list[str] = []

    if pinned is None or not inhouse_deps or not hashes:
        # The real checks above already fail closed on these preconditions;
        # nothing to mutate without them.
        return self_test_failures

    module_name, version = sorted(inhouse_deps.items())[0]

    # Mutation A: repoint this module's MODULE.bazel key at npmjs.org instead
    # of the pinned registry -- the exact shape of a supply-chain substitution.
    suffix = f"/modules/{module_name}/{version}/MODULE.bazel"
    real_key = next((key for key in hashes if key.endswith(suffix)), None)
    if real_key is not None:
        mutated_hashes = dict(hashes)
        mutated_hashes[f"https://registry.npmjs.org/EVIL{suffix}"] = mutated_hashes.pop(real_key)
        if not resolution_layer_failures(
            inhouse_deps, pinned, mutated_hashes, lock_present=True
        ):
            self_test_failures.append(
                "resolution-layer self-test failed: repointing "
                f"{module_name}@{version} MODULE.bazel at registry.npmjs.org "
                "did not trip the gate"
            )

    # Mutation B: drop registryFileHashes to empty, as a from-scratch or
    # corrupted lock would.
    if not resolution_layer_failures(inhouse_deps, pinned, {}, lock_present=True):
        self_test_failures.append(
            "resolution-layer self-test failed: an empty registryFileHashes "
            "map did not trip the gate"
        )

    # Mutation C: report the lock as absent entirely.
    if not resolution_layer_failures(inhouse_deps, pinned, hashes, lock_present=False):
        self_test_failures.append(
            "resolution-layer self-test failed: a missing MODULE.bazel.lock "
            "did not trip the gate"
        )

    return self_test_failures


def parser_self_test() -> list[str]:
    """Negative control for parse_bazel_deps(): an in-house bazel_dep whose
    `version` does not immediately follow `name` must still be seen. A parser
    that drops it fails OPEN -- the module silently escapes the
    resolution-layer audit entirely -- so this asserts order-independence
    rather than trusting the regex by inspection.
    """
    failures: list[str] = []
    fixture = (
        'bazel_dep(name = "tummycrypt_probe_a", version = "1.0.0")\n'
        'bazel_dep(name = "tummycrypt_probe_b", dev_dependency = True, version = "2.0.0")\n'
        'bazel_dep(\n    version = "3.0.0",\n    name = "tummycrypt_probe_c",\n)\n'
    )
    parsed = parse_bazel_deps(fixture)
    for name, version in (
        ("tummycrypt_probe_a", "1.0.0"),
        ("tummycrypt_probe_b", "2.0.0"),
        ("tummycrypt_probe_c", "3.0.0"),
    ):
        if parsed.get(name) != version:
            failures.append(
                "bazel_dep parser self-test failed: expected "
                f"{name}@{version}, parsed {parsed.get(name)!r}; a dropped or "
                "misparsed in-house bazel_dep would silently skip the "
                "resolution-layer audit"
            )
    return failures


def main() -> int:
    failures: list[str] = []

    # (0) The MODULE.bazel parser every check below depends on must itself be
    # trustworthy; a parser that drops deps makes checks (2) and (3) fail open.
    failures.extend(parser_self_test())

    # (1) No org-package npm specifier may remain in package.json.
    npm_specifiers = load_inhouse_npm_specifiers()
    for name, version in sorted(npm_specifiers.items()):
        failures.append(
            f"{name} is still an npm specifier ({version!r}) in package.json; "
            f"in-house packages are Bazel-only (graph-linked via npm_link_package)"
        )

    # (2) Every graph-linked org package needs both bazel_dep + npm_link_package.
    graph_linked = load_graph_linked_packages()
    bazel_deps = load_bazel_deps()
    for package_name in sorted(graph_linked):
        module_name = npm_to_bazel_module(package_name)
        if module_name not in bazel_deps:
            failures.append(
                f"{package_name} is npm_link_package'd but has no matching "
                f"bazel_dep({module_name}) in MODULE.bazel"
            )

    if not graph_linked:
        failures.append(
            "no in-house npm_link_package entries found in BUILD.bazel; "
            "expected the @tummycrypt/* packages to be graph-linked"
        )

    # (3) Resolution-layer: every in-house bazel_dep must be provably fetched
    # from the pinned bazel-registry commit, not merely declared to be.
    inhouse_deps = inhouse_bazel_deps(bazel_deps)
    pinned = load_pinned_registry()
    lock_present = MODULE_BAZEL_LOCK.exists()
    hashes: dict[str, object] | None = None
    if lock_present:
        try:
            lock = json.loads(MODULE_BAZEL_LOCK.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"MODULE.bazel.lock is not valid JSON: {exc}")
            lock = None
        if lock is not None:
            hashes = lock.get("registryFileHashes")

    if not inhouse_deps:
        failures.append(
            "no in-house bazel_dep entries found in MODULE.bazel to audit at "
            "the resolution layer"
        )
    else:
        failures.extend(
            resolution_layer_failures(inhouse_deps, pinned, hashes, lock_present=lock_present)
        )
        failures.extend(resolution_layer_self_test(inhouse_deps, pinned, hashes))

    if failures:
        print("Bazel-only ingestion check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    pin_note = f"resolution pinned to {pinned[1]}" if pinned else "resolution unpinned"
    print(
        f"Bazel-only ingestion ok: {len(graph_linked)} in-house package(s) "
        f"graph-linked (bazel_dep + npm_link_package), 0 npm specifiers in "
        f"package.json, {len(inhouse_deps)} in-house bazel_dep(s) "
        f"resolution-layer verified, {pin_note}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
