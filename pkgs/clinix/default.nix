{
  lib,
  self,
  python3Packages,
}:
python3Packages.buildPythonApplication rec {
  pname = "clinix";
  src = self;
  version = "0.0.1-${lib.flox-floxpkgs.getRev self}";
  postPatch = ''
    substituteInPlace clinix/stuff.py \
      --replace 'nix_name = ""' 'nix_name = "${pname}-${version}"'
    grep nix_name clinix/stuff.py
  '';
  PIP_DISABLE_PIP_VERSION_CHECK = 1;
  # Add Python modules needed by your package here
  propagatedBuildInputs = with python3Packages; [
    joblib
    termcolor
    requests
  ];
  makeWrapperArgs = [
    # termcolor stopped printing color at some point when invoked without
    # a controlling tty. Set the FORCE_COLOR variable to make it colorful
    # in all cases.
    "--set" "FORCE_COLOR" "1"
    # The buildPythonApplication development environment sets this variable
    # to use the local libraries in preference to those "baked into" the
    # package, but then makes it impossible to reliably test the built package
    # from within the development environment. That clearly needs some work,
    # but just clear the variable in the meantime.
    "--unset" "NIX_PYTHONPATH"
    # Capture the installation prefix and argv[0] for use at runtime.
    "--set" "NIX_SELF_PATH" "$out"
    "--run 'export NIX_ORIG_ARGV0=$0'"
  ];
  meta.description = "an example flox package";
}
