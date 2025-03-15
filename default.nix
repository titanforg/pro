{pkgs}: {
  deps = [
    pkgs.geckodriver
    pkgs.openssl
    pkgs.ffmpeg
    pkgs.python3
    pkgs.python3Packages.pip
  ];
}
