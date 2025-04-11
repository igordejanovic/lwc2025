{
  description = "Dynamic Questionnaire App with textX DSL and React frontend";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config = { allowUnfree = true; };
        };

        # Python development environment
        pythonEnv = pkgs.python311.withPackages (ps: with ps; [
          pip
          pudb
          black
          pytest
          pytest-cov
          python-lsp-server
          debugpy
        ]);

        # textXExtension = pkgs.vscode-utils.extensionFromVscodeMarketplace {
        #   name = "textX";
        #   publisher = "textX";
        #   version = "0.2.0";
        #   sha256 = "IAbtwAqXuy9cqNmdwBzYu+swOHBZ8iT16j+ZZ/Z2aRo=";
        # };

        # vscode-with-extensions = pkgs.vscode-with-extensions.override {
        #   vscodeExtensions = with pkgs.vscode-extensions; [
        #     ms-python.python
        #     ms-python.debugpy
        #     textXExtension
        #   ];
        # };

        deps = with pkgs; [
          vscode
          nodejs
          vsce
          typescript
          ruff
        ];

      in {
        devShells.default = pkgs.mkShell {
          packages = [ pythonEnv ] ++ deps;

          VIRTUAL_ENV = ".venv";

          shellHook = ''
            echo "Python environment with textX: ${pythonEnv}"
            echo "Node.js version: $(node --version)"

            # Create .env file if it doesn't exist
            if [ ! -f .env ]; then
              echo "PYTHONPATH=$PWD" > .env
              echo "Creating .env file with PYTHONPATH"
            fi

            # Create virtualenv if it doesn't exist
            if [ ! -d "$VIRTUAL_ENV" ]; then
              echo "=== Creating Python virtual env and installing deps ==="
              python -m venv "$VIRTUAL_ENV"

              # Activate the virtualenv
              source "$VIRTUAL_ENV/bin/activate"

              pip install --upgrade pip
              pip install -r requirements.txt
            else
              # Activate the virtualenv
              source "$VIRTUAL_ENV/bin/activate"
            fi

            # Add virtualenv packages to PYTHONPATH for pylint
            export PYTHONPATH="$PWD/$VIRTUAL_ENV/${pythonEnv.sitePackages}:$PYTHONPATH"

            echo "Ready for questionnaire development!"
          '';

        };
      });
}
