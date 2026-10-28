# Legalab website

Source for the Legalab website. The site is a static SvelteKit build made
with Bazel. It was spawned from the site.scaffold public template 1.0.0 and
keeps that template's Nix, Bazel and Just graph.

The site is in development and makes no product claims yet.

## Build

Run `nix develop --command just setup`, then `just dev`, `just check` or
`just build` inside that shell. `just build` runs `bazel build //:build` and
copies the output to `build/`. `just bundle` packages the same target as a
tarball.

`just contract` runs the file-only repository checks:

| Recipe | Check |
| --- | --- |
| `inhouse-package-parity` | In-house packages enter only as `bazel_dep` plus `npm_link_package`, and `MODULE.bazel.lock` resolves them from the pinned registry commit |
| `estate-versions` | `package.json` framework pins match `estate/versions.json` |

## Dependencies

First-party modules resolve from the public `xoxd-ai/bazel-registry` at the
commit pinned in `.bazelrc`, then from the Bazel Central Registry. Third-party
packages come from the frozen pnpm lock. `package.json` carries no
`@tummycrypt` or `@xoxd` specifier.

| Module | Version | Use |
| --- | --- | --- |
| `xoxd_public_chrome` | 0.1.0 | navigation, footer and theme picker |
| `xoxd_theme` | 0.1.1 | theme tokens and fonts |
| `tummycrypt_vite_plugin_a11y` | 0.2.4 | build-time accessibility checks |
| `tummycrypt_vite_plugin_skeleton_colors` | 0.2.4 | Skeleton colour utilities |
| `tummycrypt_tinyland_color_utils` | 0.2.3 | colour helpers |
| `tummycrypt_tinyvectors` | 0.3.7 | vector backgrounds |

## Routes

| Route | State |
| --- | --- |
| `/` | stub |
| `/about` | stub |
| `/links` | stub, renders `rel="me"` profile links once accounts exist |
| `/privacy` | stub, no policy in force |
| `/terms` | stub, no terms in force |

## Content rules

This repository is public. It holds no customer data, host names, private
paths, secrets or deployment manifests. Product pages carry only claims backed
by published evidence. Deployment lives in a separate owner overlay.

## Licence

MIT, see `LICENSE` and `NOTICE`.
