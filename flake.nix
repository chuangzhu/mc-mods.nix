{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.05";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }: flake-utils.lib.eachDefaultSystem (system: {
    legacyPackages = import ./. { nixpkgs = nixpkgs.legacyPackages.${system}; };
  }) // { overlays.default = import ./overlay.nix; };
}
