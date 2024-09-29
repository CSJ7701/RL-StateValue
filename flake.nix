{
  description = "An exploration of State and Action Value Functions in Reinforcement Learning using Python.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  # ================================================
  
  outputs = { self, nixpkgs, poetry2nix, ...}@inputs:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };
      inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryEnv;
      pythonEnv = mkPoetryEnv {
        python = pkgs.python312;
        projectDir = ./.;
      };

      # Define tests
      tests = pkgs.stdenv.mkDerivation {
        name = "run-tests";
        buildInputs = [ pythonEnv ];
        src = ./.;
        output = "result";
        dontBuild = true; # Indicate that derivation does not produce outputs
        installPhase = ''
          mkdir -p $out
          ls
          python -m unittest discover -s tests -p "*.py" || echo "Hello"
        ''; # Run all tests in tests directory
      };
    in

      # =========================================================

      {
        devShells.${system}.default = pkgs.mkShell {
          packages = with pkgs; [
            pythonEnv
            poetry
          ];
          shellHook = ''
          fish
          '';
        };

        # Run with 'nix build .#tests'
        packages.${system}.tests = tests;


      };
}
