import os

import yaml

from . import save_url_image


def parse_issue_body(body):
    """
    Parse the body of the issue and return a dictionary of the parsed data.
    """
    parsed = {}
    k = None

    for line in body.split("\n"):
        if line.startswith("###"):
            k = line.removeprefix("###").strip().lower().replace(" ", "_")
            parsed[k] = ""
        else:
            if k is not None:
                parsed[k] += line.strip()

    return parsed


def format_site_label(name):
    if name == "github":
        return "GitHub"
    elif name in ['twitter', 'scholar', 'website']:
        return name.title()
    else:
        return name

def format_parsed_content(parsed):
    """
    Format the parsed content into a string.
    """
    parsed["alumni"] = parsed["status"] == "Alumni"

    parsed["links"] = [
        {"label": format_site_label(key), "url": parsed[key]}
        for key in ["website", "twitter", "github", "scholar"]
        if parsed[key] != "_No response_"
    ]

    keys_removed = ["status", "website", "twitter", "github", "scholar"]

    return {k: v for k, v in parsed.items() if v != "_No response_" and k not in keys_removed}

if __name__ == "__main__":
    issue_body = os.environ['ISSUE_BODY']

    parsed = parse_issue_body(issue_body)
    profile = format_parsed_content(parsed)

    authors = yaml.safe_load(open("_data/authors.yml"))

    if profile["name"] not in authors:
        key = profile["name"]
    else:
        n = 2
        while (k := f'{profile["name"]} {n}') in authors:
            n += 1
        key = k

    save_url_image(fname=key, profile=profile, key="avatar", path='assets/images/bio')

    with open("_data/authors.yml", "a") as f:
        f.write("\n")
        yaml.dump({key: profile}, f)
