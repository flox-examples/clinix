{
  lib,
  self,
  python3Packages,
}:
python3Packages.buildPythonApplication {
  pname = "clinix";
  src = self;
  version = builtins.trace "0.0.1-${lib.flox-floxpkgs.getRev self}" "0.0.1-r${toString self.revCount or "dirty"}";
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
    # also capture the installation prefix and argv[0] for use at runtime.
    "--set" "NIX_SELF_PATH" "$out"
    "--run 'export NIX_ORIG_ARGV0=$0'"
  ];
  meta.description = "an example flox package";
}
