
from __future__ import print_function

import sys, os, json
from datetime import datetime
import requests
import json
from joblib import Memory
user = os.environ.get('USER')
memory = Memory(f"/tmp/{user}", verbose=0)

@memory.cache
def geolocation_data():
    # Attempt until we're successful
    while True:
        try:
            # get my real ip address
            ip_address = requests.get("https://api.ipify.org/?format=json").json()['ip']
            # look up my geolocation info
            request_url = f"https://geolocation-db.com/jsonp/{ip_address}"
            response = requests.get(request_url)
            result = response.content.decode()
            result = result.split("(")[1].strip(")")
            return json.loads(result)
        except:
            pass

def get_runtime_info():
    ret = {}

    # We lose argv0 when going through the nix wrapper so instead report the
    # values as saved/exported by the nix wrapper itself.
    ret["argv0"] = os.environ.get('NIX_ORIG_ARGV0') or sys.argv[0]
    ret["abspath"] = os.path.abspath(ret["argv0"])
    ret["realpath"] = os.path.realpath(ret["argv0"])
    nix_name = "" # updated at Nix build time
    if nix_name != "":
        ret["nix_name"] = nix_name

    ret["isnix"] = ret["realpath"].startswith("/nix/store/")

    if ret["isnix"]:
        elts = ret["realpath"].split("/")
        ret["nixpkg"] = elts[3]

        # A future feature: recording of source info in built package.
        flox_json = "/nix/store/" + ret["nixpkg"] + "/.flox.json"
        if os.path.exists(flox_json):
            data = json.load(open(flox_json))
            for k in ["rev", "date"]:
                if k in data:
                    ret["git"+k] = data[k]
            if "url" in data:
                giturl = data["url"]
                giturl = giturl.replace("https://github.com/", "github:")
                ret["giturl"] = giturl
            if "version" in data:
                ret["version"] = data["version"]



    for key, value in geolocation_data().items():
        ret[key] = value

    if ret["argv0"] == ret["abspath"]:
        del ret["abspath"]

    ret["time"] = datetime.now().strftime("%H:%M:%S")

    return ret
