set shell := ["bash", "-euo", "pipefail", "-c"]
root := justfile_directory()
export USE_BAZEL_VERSION := `cat .bazelversion`

_default:
    @just --list

setup:
    cd {{ root }} && pnpm install --frozen-lockfile
    just deps-graph
    just workspace-types

# Materialize the same declared public packages for live Vite/editor commands.
deps-graph:
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{ root }}
    mapfile -t graph_packages < <(bazelisk query 'filter("^//:node_modules/(@xoxd|@tummycrypt)/[^/]+$", //:*)' --output=label)
    (( ${#graph_packages[@]} > 0 ))
    bazelisk build "${graph_packages[@]}"
    for graph_package in "${graph_packages[@]}"; do
        package_path="${graph_package#//:}"
        mkdir -p "$(dirname "$package_path")"
        ln -sfn "$(realpath "bazel-bin/$package_path")" "$package_path"
    done

workspace-types:
    cd {{ root }} && bazelisk build //:sveltekit_types
    cd {{ root }} && python3 scripts/bazel_output.py materialize --source bazel-bin/.svelte-kit --destination .svelte-kit --required-path types/route_meta_data.json
    cd {{ root }} && python3 scripts/bazel_output.py materialize --source 'bazel-bin/node_modules/$app' --destination 'node_modules/$app' --required-path tsconfig.json

deps-lock:
    cd {{ root }} && pnpm install --lockfile-only

bazel-lock:
    cd {{ root }} && bazelisk --batch mod deps --lockfile_mode=update

# Interactive dev server: local by design, bounded by the .bazelrc idle limit.
dev port="5173": deps-graph workspace-types
    cd {{ root }} && bazelisk run //:dev -- --port {{quote(port)}} --strictPort

build:
    cd {{ root }} && bazelisk build //:build
    cd {{ root }} && python3 scripts/bazel_output.py materialize --source bazel-bin/build --destination build

# Bounded local check (R471): no remote fallback, no upload, and no
# claim of flywheel evidence until this site enrolls a flywheel lane.
check: contract
    @echo "check: local, non-qualifying (no enrolled flywheel lane)"
    cd {{ root }} && bazelisk test //:svelte_check_test --remote_local_fallback=false --noremote_upload_local_results

# Repository contract checks. They read files only and run no build.
contract: inhouse-package-parity estate-versions

# In-house packages enter only as bazel_dep plus npm_link_package, and the
# lock must resolve them from the pinned registry commit.
inhouse-package-parity:
    cd {{ root }} && python3 scripts/check-inhouse-package-parity.py

# Framework pins match the estate manifest copied in estate/versions.json.
estate-versions:
    cd {{ root }} && python3 scripts/check-estate-versions.py

preview port="4173": build
    cd {{ root }} && python3 scripts/bazel_output.py preview --port {{ port }}

bundle:
    cd {{ root }} && bazelisk build //:deployment_bundle
