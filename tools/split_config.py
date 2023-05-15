#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from pathlib import Path
import yaml


def dump_project(dest, prj_type: str, project, config=None):
    """Write project config file"""
    (prj_org, prj_repo_name) = project.split("/")
    prj_dst = Path(dest, prj_type, prj_org)
    prj_dst.mkdir(parents=True, exist_ok=True)
    with open(Path(prj_dst, f"{prj_repo_name}.yaml"), "w") as fp:
        if config:
            yaml.dump(config, fp)


def split(fname: str, dest: str):
    """Split single tenants file into the file hierarchy"""
    with open(Path(fname), "r") as fp:
        data = yaml.safe_load(fp)

    for item in data:
        auth_rule = item.get("authorization-rule", item.get("admin-rule"))
        tenant = item.get("tenant")
        if tenant:
            tenant_name = tenant["name"]
            dst = Path(dest, "tenants", tenant_name)
            dst.mkdir(parents=True, exist_ok=True)
            for sk, sv in tenant.get("source").items():
                s_dst = Path(dst, "sources", sk)
                s_dst.mkdir(parents=True, exist_ok=True)
                for prj_type in ["config-projects", "untrusted-projects"]:
                    for prj_item in sv.get(prj_type, []):
                        prj_config = None
                        prj_name = None
                        if isinstance(prj_item, dict):
                            if "projects" in prj_item:
                                # project group - split into individual entries
                                group_config = copy.deepcopy(prj_item)
                                group_config.pop("projects")
                                for prj in prj_item["projects"]:
                                    dump_project(
                                        s_dst,
                                        prj_type,
                                        prj,
                                        config=group_config,
                                    )
                            else:
                                # simple dict with project config
                                prj_name = list(prj_item.keys())[0]
                                prj_config = prj_item[prj_name]
                        else:
                            # simple string with project name
                            prj_name = prj_item

                        if prj_name:
                            dump_project(
                                s_dst, prj_type, prj_name, config=prj_config
                            )

            with open(Path(dst, "tenant.yaml"), "w") as fp:
                tenant_content = copy.deepcopy(tenant)
                tenant_content.pop("source")
                yaml.dump(tenant_content, fp)

        if auth_rule:
            dst = Path(dest, "auth-rules")
            dst.mkdir(parents=True, exist_ok=True)
            with open(Path(dst, f"{auth_rule['name']}.yaml"), "w") as fp:
                yaml.dump(auth_rule, fp)


def main():
    split("zuul/main.yaml", "zuul")


if __name__ == "__main__":
    main()
