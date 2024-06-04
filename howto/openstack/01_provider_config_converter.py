#!/usr/bin/python3

import pathlib
import json
import yaml

clouds = pathlib.Path("clouds.yaml")

if not clouds.exists:
    exit("You need a clouds.yaml from your OpenStack project in this directory")


creds = dict()
with clouds.open("r") as fh:
    doc = yaml.safe_load(fh)
    c = doc["clouds"]["openstack"]["auth"]
    creds = {
        "auth_url": c["auth_url"],
        "application_credential_id": c["application_credential_id"],
        "application_credential_secret": c["application_credential_secret"],
        "tenant_name": "centralapiuser"
    }

docs_to_write = list()
with open("01_provider_config.yaml.tmpl") as fh:
    alldocs = yaml.safe_load_all(fh)
    for doc in alldocs:
        if doc["kind"] == "Secret":
            doc["stringData"]["clouds.json"] = json.dumps(creds)
            docs_to_write.append(doc)
        else:
            docs_to_write.append(doc)

generated_path = pathlib.Path("generated")
if not generated_path.exists():
    generated_path.mkdir(mode=0o755)

with open("generated/01_provider_config.yaml", "w") as fh:
    yaml.safe_dump_all(docs_to_write, fh, default_flow_style=False)
