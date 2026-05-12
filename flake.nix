{
  description = "5QLN Foundation Constitutional Substrate — reproducible verifier builds";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        # Development shell with all toolchains pinned
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python311
            python311Packages.pytest
            python311Packages.jsonschema
            nodejs_20
            cargo
            rustc
            git
            openssl
            coreutils
            jq
          ];

          shellHook = ''
            echo
            echo "5QLN Foundation reproducible dev shell"
            echo "  Python:  $(python3 --version)"
            echo "  Node:    $(node --version)"
            echo "  Rust:    $(rustc --version)"
            echo
            echo "Run: ./scripts/seal-phase-0.sh --verify-only"
            echo
          '';
        };

        # Verifier builds (one per language) — each must produce identical hash output
        packages = {
          verify-python = pkgs.writeShellScriptBin "verify-codex-py" ''
            ${pkgs.python311}/bin/python3 ${./tools/python/verify_codex.py} "$@"
          '';

          verify-node = pkgs.writeShellScriptBin "verify-codex-node" ''
            ${pkgs.nodejs_20}/bin/node ${./tools/node/verify-codex.mjs} "$@"
          '';

          verify-rust = pkgs.rustPlatform.buildRustPackage {
            pname = "verify-codex";
            version = "0.1.0";
            src = ./tools/rust;
            cargoLock.lockFile = ./tools/rust/Cargo.lock;
          };

          # Convenience: verify the canonical codex.txt
          verify = pkgs.writeShellScriptBin "verify-codex" ''
            CODEX="${./codex/codex.txt}"
            echo "Verifying $CODEX with all three implementations..."
            ${pkgs.python311}/bin/python3 ${./tools/python/verify_codex.py} "$CODEX"
            ${pkgs.nodejs_20}/bin/node ${./tools/node/verify-codex.mjs} "$CODEX"
            echo
            echo "All implementations agree."
          '';

          default = self.packages.''${system}.verify;
        };

        # Checks run by `nix flake check`
        checks = {
          verify-canonical = pkgs.runCommand "verify-canonical" {
            buildInputs = [ pkgs.python311 ];
          } ''
            python3 ${./tools/python/verify_codex.py} ${./codex/codex.txt}
            touch $out
          '';
        };
      });
}
