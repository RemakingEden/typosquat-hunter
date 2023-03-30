#!/bin/python3

import requests
import json
import jellyfish
import sys

app_dir = "/app"
levenshtein_number = 1
PyPi_list_url = "https://raw.githubusercontent.com/vincepower/python-pypi-package-list/main/pypi-packages.json"


def get_requirements(filename):
    packages = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            package = (
                line.split(" ", 1)[0]
                .split(",", 1)[0]
                .split("==", 1)[0]
                .split(">=", 1)[0]
            )
            packages.append(package)
    return packages


def get_whitelist(filename):
    whitelist = set()
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            whitelist.add(line)
    return whitelist


def get_packages():
    response = requests.get(
        PyPi_list_url
    )
    try:
        data = response.json()
        packages = data["packages"]
    except (json.decoder.JSONDecodeError, KeyError):
        packages = []
    return packages


def get_downloads(package):
    response = requests.get(f"https://pypistats.org/api/packages/{package}/recent")
    if response.status_code == 200:
        try:
            data = response.json()
            downloads = data["data"]["last_month"]
        except (json.decoder.JSONDecodeError, KeyError, ValueError):
            downloads = 0
    else:
        downloads = 0
    return downloads


def get_similar_packages(package, packages, levenshtein_number):

    similar_packages = []
    for p in packages:
        distance = jellyfish.levenshtein_distance(package, p)
        if distance <= levenshtein_number:
            similar_packages.append(p)
    return similar_packages


def compare_downloads(package, similar_packages):
    suspicious_packages = {}
    original_downloads = get_downloads(package)
    for p in similar_packages:
        similar_downloads = get_downloads(p)
        if similar_downloads > original_downloads:
            suspicious_packages[p] = package
    return suspicious_packages


def main():
    print("Parsing requirements")
    requirements = get_requirements(f"{app_dir}/requirements.txt")
    whitelist = get_whitelist(f"{app_dir}/typohunterwhitelist.txt")
    print("Getting all packages")
    packages = get_packages()
    warn_packages = {}
    for package in requirements:
        if package in whitelist:
            print(
                f"Skipping the package {package} as it is included in the whitelist"
            )
            continue
        print(f"Assessing {package} for typosquatting")
        similar_packages = get_similar_packages(package, packages, levenshtein_number)
        warn_packages.update(compare_downloads(package, similar_packages))
    if warn_packages:
        print("\nWarning: The following packages may be typosquatted versions of genuine packages:")
        for k, v in warn_packages.items():
            print(f"- {v} may be imitating {k}")
        sys.exit(1)
    else:
        print("No suspicious packages found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
