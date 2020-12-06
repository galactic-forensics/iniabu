# Contributing

Everybody is welcome
to contribute to this project.
Please make sure you have read
our [Code of Conduct](CODE_OF_CONDUCT.md).
You are expected to adhere to it.

Here we only give the short version
on how to contribute to the `iniabu` project.
A detailed developers guide
can be found
[here](https://iniabu.readthedocs.io/en/latest/dev/index.html).

## Nox

[Nox](https://nox.thea.codes/en/stable/) is used
to automate testing.
A configuration `noxfile.py`
is provided in the repository.
To get a list of all installed
development environments type:

```console
nox
```

## Code format

We use black,
version 20.8b1,
to automatically format the code.
To adhere to these formatting guidelines,
you can run black by typing:

```console
nox -s black
```

## Linting

Code is linted according to `flake8` specifications.
To run the linter, type:

```console
nox -s lint
```

## Testing

To test the package,
[pytest](https://docs.pytest.org/en/latest/)
is used.
Please make use of
[hypothesis](https://hypothesis.readthedocs.io/en/latest/)
where adequate.
Also check out the existing tests
to see what structure, etc.,
we strive for.

Certain plugins,
as specified in `dev-requirements.txt`
are required for local testing.
The codebase is tested for compatibility
with Python 3.6+.
To run all tests,
type:

```console
nox -s tests
```

In addition to package testing,
you can also test all docstring examples
by using xdoctests.
To do so type:

```console
nox -s xdoctest
```

This ensures that all docstring examples
are actually working.

## Documentation

Sphinx is used
to automatically create our
[documentation](https://iniabu.rtfd.io).
If you want to build it locally,
nox is setup to do so.
Type:

```console
nox -s docs
```

## Pull requests

It is advisable to discuss a feature enhancement,
issue, etc. via raising an issue first.
Feel free to create pull requests.
All pull requests are tested
using GitHub actions upon submission.
Mandatory tests that are required to pass
are the following nox sessions:

- lint
- tests
- safety
- xdoctest

Thus: please ensure you test these
prior to submitting a pull request.
