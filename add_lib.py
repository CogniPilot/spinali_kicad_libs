#!/usr/bin/env python3

import json
import platform
import os
import sys
import argparse
import jinja2

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--overwrite", action='store_true', help="Overwrites all libraries in environment.var")
parser.add_argument("-k", "--kicad_ver", type=str, default="9.0", help="Kicad version to apply library to (defaults to 9.0)")
parser.add_argument("-a", "--kicad_alias", type=str, default="SPINALI", help="Library alias name (defaults SPINALI)")
args = parser.parse_args()

lib_path = os.path.dirname(os.path.abspath(__file__))

if platform.system() == 'Windows':
    print("Running on Windows")
    kicad_config_file = os.path.abspath(f"%Appdata%/kicad/{args.kicad_ver}/kicad_common.json")
elif platform.system() == 'Linux':
    print("Running on Linux")
    kicad_config_file = os.path.abspath(os.path.expanduser(f"~/.config/kicad/{args.kicad_ver}/kicad_common.json"))
else:
    print(f"Running on an unknown OS: {platform.system()}")
    sys.exit(1)

if not os.path.isfile(kicad_config_file):
    print(f"Failed to find the config file at: {kicad_config_file}")
    sys.exit(1)

lib_json_entry = """
{{ "{" }} "KICAD_{{ alias_name }}": "{{ lib_path }}"
{%- if dir_3d -%}
, "{{ alias_name }}_3DMODEL_DIR": "${{ "{" }}KICAD_{{ alias_name }}{{ "}" }}/3dmodels"
{%- endif -%}
{%- if dir_fp -%}
, "{{ alias_name }}_FOOTPRINT_DIR": "${{ "{" }}KICAD_{{ alias_name }}{{ "}" }}/footprints"
{%- endif -%}
{%- if dir_sy -%}
, "{{ alias_name }}_SYMBOL_DIR": "${{ "{" }}KICAD_{{ alias_name }}{{ "}" }}/symbols"
{%- endif -%}
{{ " }" }}
"""

try:
    with open(kicad_config_file, 'r') as config_file_read:
        config_data = json.load(config_file_read)
    
    template = jinja2.Template(lib_json_entry)
    config_to_add = template.render(
        alias_name=args.kicad_alias.upper(), 
        dir_3d=os.path.isdir(os.path.join(lib_path,"3dmodels")),
        dir_fp=os.path.isdir(os.path.join(lib_path,"footprints")),
        dir_sy=os.path.isdir(os.path.join(lib_path,"symbols")),
        lib_path=lib_path
        )

    lib_config = config_data["environment"]["vars"]

    if lib_config:
        print("Libraries currently set to:")
        print(json.dumps(lib_config, indent=4))
        if args.overwrite:
            print(f"Overwriting all lib entries.")
            lib_config=json.loads(config_to_add)
        else:
            print(f"Updating to include current lib with existing libs.")
            lib_config.update(json.loads(config_to_add))
    elif not lib_config:
        print(f"No existing libs found, adding current lib.")
        lib_config=json.loads(config_to_add)

    config_data["environment"]["vars"] = lib_config

    with open(kicad_config_file, 'w') as config_file_write:
        json.dump(config_data, config_file_write, indent=4)

except Exception as e:
        print(f"An unexpected error occurred: {e}")
print("Libraries updated to:")
print(json.dumps(config_data["environment"]["vars"], indent=4))
