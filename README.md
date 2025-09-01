# TempCatcher, indentify spam emails on clean domains.

## What is TempCatcher?
TempCatcher is a service which provides intelligence on temporary email addresses.

## Why use TempCatcher? 
Our service is the logical next step If you have exhausted all other solutions in your battle against spam (domain whitelisting / blacklisting).

## How do i use TempCatcher?
Please refer to [quick start guide](https://github.com/tempcacher/tempcatcher/README.md#quick-start-guide)

## Where do you get your data?
We aggregate our data from a variety of known spam providers.

## Do you offer any paid services?
Yes, we offer a more simple "checks" api which allows you to send an email via http(s) and check if that is in our database.

For enterprise customers also provide intelligence on phone numbers as well.

if you are interested in these services please email contact@tempcatcher.com

---

# Quick Start guide
## 1) Install TempCatcher api.

`pip install tempcatcher`

## 2) Example code:
```python
from tempcatcher import *
t = TempCatcher(update = 60) # update every 60 seconds

status = t.check(input("Input email you would like to check: "))

match status:
  case 0:
    print("Email was found in the tempcatcher data. (spam)")
  case 1:
    print("Email was not found in the tempcatcher data. (not spam)")
  case 2:
    print("Email was formatted incorrectly.")
  case 3:
    print(f"Email: `{email}` Could not find DNS MX record assocciated with domain")
  case _:
    print("How did we get here?")
del t
```
