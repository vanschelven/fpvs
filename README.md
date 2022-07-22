## Fast Python Vulnerability Scanner

Use the GitLab Advisory Database to do Python Vulnerability Scanning.

This looks quite similar to what [Gitlab's Gemnasium Dependency Scanning
Analyzer](https://gitlab.com/gitlab-org/security-products/analyzers/gemnasium)
does, but comes with some differences:

* No Docker container is included in this project. Bring your own or work locally.
* Results are printed on stdout, and are directly readable.
* Works on a directory of already vendored wheels rather than doing
  `pip install -r requirements.txt` in some half-baked attempt to determine the
  results of such a call.

Why a single command, rather than a full blown Docker container?

1. You should generally ask the opposite question. Now get off my lawn.
2. Ability to trivially run from your local development environment.
3. No working around the limitations of missing header files when trying
   to get `pip install some-package-without-wheel-but-with-c-bindings` to work.
4. Fast: just reuse already-vendored packages (from some cache or artifact)
   rather than doing yet another `pip install -r requirements.txt` in each job
   of your pipeline.

usage: `fpvs-scan [-h] [--wheels-path WHEELS_PATH] [--gemnasium-db-path GEMNASIUM_DB_PATH] [--version] [--verbose]`

Example usage:

```
# 1. install the wheels to be scanned
pip install wheel
pip wheel requests==2.0.1 --wheel-dir=vendor  # this is a bad package on purpose, to show off what FPVS does

# 2. get fpvs, the vulnerability database and do the scanning:
pip install fpvs
git clone git@gitlab.com:gitlab-org/security-products/gemnasium-db.git
fpvs-scan --verbose
```

In typical real-world usage, part 1 of the example above would already be
executed in some other part of your pipeline or development flow, and would
have become an artifact / just live on your machine. This is what makes FPVS
fast: it doesn't do slow stuff that you did already.

Example output:

```
fpvs-scan  --verbose
Checking wheels in vendor against gemnasium-db
SCANNING requests-2.0.1-py2.py3-none-any.whl
ADVISORY pypi/requests/CVE-2014-1829.yml: 2.0.1 against <=2.2.1 FAIL
ADVISORY pypi/requests/CVE-2013-2099.yml: 2.0.1 against <=1.0.3 OK
ADVISORY pypi/requests/CVE-2018-18074.yml: 2.0.1 against <2.20.0 FAIL
ADVISORY pypi/requests/GMS-2012-3.yml: 2.0.1 against <0.12.0 OK
ADVISORY pypi/requests/CVE-2014-1830.yml: 2.0.1 against <=2.2.1 FAIL
ADVISORY pypi/requests/CVE-2015-2296.yml: 2.0.1 against <2.6.0 FAIL

pypi/requests
Information Exposure
Requests (aka python-requests) allows remote servers to obtain a netrc password by reading the Authorization header in a redirected request.
CVE-2014-1829
Upgrade to version 2.3.0 or above.

pypi/requests
Information exposure in HTTP headers
The Requests package for Python sends an HTTP Authorization header to an HTTP URI upon receiving a same-hostname https-to-http redirect, which makes it easier for remote attackers to discover credentials by sniffing the network.
CVE-2018-18074
Upgrade to version 2.20.0 or above.

pypi/requests
Information Exposure
Requests (aka python-requests) allows remote servers to obtain sensitive information by reading the Proxy-Authorization header in a redirected request.
CVE-2014-1830
Upgrade to version 2.3.0 or above.

pypi/requests
Session fixation in resolve_redirects()
The `resolve_redirects()` function in `sessions.py` allows a remote, user-assisted attacker to conduct a session fixation attack. This flaw exists because the application, when establishing a new session, does not invalidate an existing session identifier and assign a new one. With a specially crafted request fixating the session identifier, a context-dependent attacker can ensure a user authenticates with the known session identifier, allowing the session to be subsequently hijacked.
CVE-2015-2296
Upgrade to version 2.6.0 or above.

FAILURE: Found 4 advisories
```

Note that the GitLab Advisory Database has a [licence that is separate from the
FPVS](https://gitlab.com/gitlab-org/security-products/gemnasium-db/-/blob/master/LICENSE.md).
