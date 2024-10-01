{
  description = "An exploration of State and Action Value Functions in Reinforcement Learning using Python.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, ...}@inputs:
    flake-utils.lib.eachDefaultSystem (system:
      let
        myapp = { poetry2nix, lib }: poetry2nix.mkPoetryApplication {
          projectDir = self;
        };
        system = "x86_64-linux";
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            poetry2nix.overlays.default
            (final: _: {
              myapp = final.callPackage myapp { };
            })
          ];
        };

      in

        {
          packages.default = pkgs.myapp;
          devShells = {
            default = pkgs.mkShell {
              packages = with pkgs; [
                poetry
              ];
              inputsFrom = [ pkgs.myapp ];
              shellHook = ''fish'';
            };

            poetry = pkgs.mkShell {
              packages = [ pkgs.poetry ];
            };

            test = pkgs.mkShell {
              inputsFrom = [pkgs.myapp ];
              shellHook = ''python -m unittest discover -s tests -p "*.py" && exit'';
            };

          };
          legacyPackages = pkgs;
        }
    );
}
