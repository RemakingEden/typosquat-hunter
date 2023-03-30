# Typosquat Hunter POC

Typosquat Hunter is a Python app that helps you find typosquatting in packages during CI. Typosquatting is a malicious practice of registering names that are similar to existing ones, such as `requets` instead of `requests`, in order to trick users into installing them. Typosquat Hunter compares the packages in your dependencies and flags if it thinks any may be suspicious.

## Roadmap

- [x] Proof of concept
    This is a proof this can work and if anyone wants it. I have built the app really scrappy but just enough so it works. It only works with PyPi and is taking in very few data points to decide if a package is a typosquatter or not. I think in its current state it would be frustrating the amount of false positives that could arise especially if using a more niche package.

- [ ] Minimum Viable Product
    If people found TypoSquat Hunter useful I would rebuild the app from scratch perhaps in a more performant language. I would try to build it in a modular way so we can add new libraries and packaging systems as we go. I would also like to take in more data points from the packages such as date of upload to more accurately predict malicious packages.

... Onwards


## Run Locally

Clone the project

```bash
  git clone https://github.com/RemakingEden/typosquat-hunter
```

Go to the project directory

```bash
  cd typosquat-hunter
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Change the path of the app variable to point at the app you want to scan. This is hardcoded to /app currently.

```
  app_dir = /your/app/location
```

Run the script

```bash
./typosquatHunter.py
```

If you would like to ignore a package as false positive you can add this package to a whitelist called `typosquathunterwhitelist.txt` in the app folder

## Reason for creation

I have been hearing more and more about attacks from typosquatting packages and it surprised me when I tried looking for a solution that could spot these in CI. I thought there could be enough data provided to spot some if not most typosquatting packages. If you'd like to know more about the ways typosquatting can be used to attack projects check out the below articles.

- [How Adversaries Attack APIs Through Dependencies](https://danaepp.com/how-adversaries-attack-apis-through-dependencies)
- [Typosquat campaign mimics 27 brands to push Windows, Android malware](https://www.bleepingcomputer.com/news/security/typosquat-campaign-mimics-27-brands-to-push-windows-android-malware/)

## Feedback

This is a basic POC to hopefully get some feedback and ideas. If you have any please feel free to create a PR and we can talk them through.


