{ pkgs ? import <nixpkgs> {}}:

pkgs.mkShell {
  buildInputs = [
    pkgs.glibcLatest
    pkgs.ffmpeg
  ];
}
