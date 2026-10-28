{
  description = "Public site.scaffold development shell";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { nixpkgs, flake-utils, ... }: flake-utils.lib.eachDefaultSystem (system:
    let pkgs = nixpkgs.legacyPackages.${system}; in {
      devShells.default = pkgs.mkShell { packages = with pkgs; [nodejs_22 pnpm just git bazelisk python3];
        shellHook = ''
          export PATH="${pkgs.bazelisk}/bin:$PATH"
          export USE_BAZEL_VERSION="$(cat .bazelversion)"
          corepack enable >/dev/null 2>&1 || true
        ''; };
      formatter = pkgs.nixpkgs-fmt;
    });
}
