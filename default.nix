{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.glibc
    pkgs.glibcLocales
    pkgs.ffmpeg
  ];
}
