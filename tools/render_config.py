#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import yaml


def merge(src: str):
    """Merge file hierarchy into single tenant config"""
    zuul_config = list()
    tenants_src = Path(src, "tenants")
    for tenant in tenants_src.glob("*/tenant.yaml"):
        # Loop over found tenants
        tenant_root = tenant.parent
        with open(tenant, "r") as fp:
            tenant_config = yaml.safe_load(fp)
            tenant_config.setdefault("source", dict())
            for project in Path(tenant_root, "sources").glob("**/*.yaml"):
                (
                    _,
                    source_name,
                    prj_type,
                    org_name,
                    repo_name,
                ) = project.relative_to(tenant_root).parts
                source = tenant_config["source"].setdefault(
                    source_name,
                    {"config-projects": list(), "untrusted-projects": list()},
                )
                project_config = dict()
                with open(project, "r") as fp:
                    project_config = yaml.safe_load(fp)
                if project_config:
                    project_data = {
                        f"{org_name}/{project.stem}": project_config
                    }
                else:
                    project_data = f"{org_name}/{project.stem}"
                source[prj_type].append(project_data)
        zuul_config.append({"tenant": tenant_config})

    auth_rules_src = Path(src, "auth-rules")
    for auth_rule in auth_rules_src.glob("*.yaml"):
        rule_data = None
        with open(auth_rule, "r") as fp:
            rule_data = yaml.safe_load(fp)
        zuul_config.append({"authorization-rule": rule_data})

    return zuul_config


def main():
    config = merge("zuul")
    print(yaml.dump(config))


if __name__ == "__main__":
    main()
