{ nixpkgs ? import <nixpkgs> { } }:

with nixpkgs.lib;

let
  license2nix = with licenses; string:
    if string == "apache" then asl20 else
    if string == "arr" then unfree else
    if string == "bsd-3-clause" then bsd3 else
    if string == "cc0" then cc0 else
    if string == "custom" then "custom" else
    if string == "gpl-2" then gpl2 else
    if string == "gpl-3" then gpl3 else
    if string == "isc" then isc else
    if string == "lgpl-2.1" then lgpl21 else
    if string == "lgpl-3" then lgpl3 else
    if string == "mit" then mit else
    if string == "mpl-2" then mpl20 else
    if string == "unlicense" then unlicense else
    if string == "zlib" then zlib else string;
in

mapAttrs' (gameversion: loaders: nameValuePair "v${replaceChars ["."] ["_"] gameversion}"
  (builtins.mapAttrs (loader: mods:
    builtins.mapAttrs (slug: info: nixpkgs.fetchurl {
      inherit (info) url sha512;
      meta = { inherit (info) description; license = license2nix info.license; };
    }) mods
  ) loaders)
) (builtins.fromJSON (builtins.readFile ./modrinth.json))
