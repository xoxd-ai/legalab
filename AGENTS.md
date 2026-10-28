# Legalab website contract

This repository is public. Read this file before any change.

- Build through Bazel. `just build` runs `//:build`. Do not add a parallel
  npm or pnpm build path.
- In-house packages enter only as a `bazel_dep` from the pinned registry plus
  an `npm_link_package` entry. `just inhouse-package-parity` enforces it.
- Framework pins follow `estate/versions.json`. `just estate-versions`
  enforces it.
- Keep host names, private paths, IP addresses, customer data, client text,
  unreleased art and secrets out of tracked files, commits and logs.
- Product, performance and safety claims appear only with published
  evidence. Do not add one by hand.
- The repository ships no deployment manifest and no credential.
- Sign commits, add a sign-off and cite the tracking ticket.
