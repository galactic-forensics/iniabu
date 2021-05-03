"""Configuration file for testing the package with ``nox``."""

import nox


nox.options.sessions = "lint", "safety", "tests", "xdoctest"

package = "iniabu"
locations = "iniabu", "tests", "noxfile.py", "docs/conf.py"
python_suite = ["3.9", "3.8", "3.7", "3.6"]
python_main = "3.9"


@nox.session(python=python_main)
def black(session):
    """Autoformat all python files with black."""
    args = session.posargs or locations
    session.install("--upgrade", "pip")
    session.install("black==20.8b1")
    session.run("black", *args)


@nox.session(python=python_main)
def build(session):
    """Pack iniabu for release on PyPi."""
    session.install("flit")
    session.run("flit", "build")


@nox.session(python=python_main)
def docs(session):
    """Build the documentation."""
    session.install("--upgrade", "pip")
    session.install("sphinx", "sphinx_rtd_theme", "-r", "requirements.txt", "pytest")
    session.chdir("docs")
    session.run(
        "sphinx-build", "-b", "html", ".", "_build/html/"
    )  # as for readthedocs.io


@nox.session(python=python_main)
def lint(session):
    """Lint project using ``flake8``."""
    args = session.posargs or locations
    session.install("--upgrade", "pip")
    session.install("-r", "dev-requirements.txt")
    session.run("flake8", *args)


@nox.session(python=python_suite)
def tests(session):
    """Test the project using ``pytest``."""
    session.install("--upgrade", "pip")
    session.install("-r", "requirements.txt", "-r", "dev-requirements.txt")
    session.run("pytest")


@nox.session(python=python_main)
def safety(session):
    """Safety check for all dependencies."""
    session.install("--upgrade", "pip")
    session.install("safety", "-r", "requirements.txt", "-r", "dev-requirements.txt")
    session.run(
        "safety",
        "check",
        "--full-report",
    )


@nox.session(python=python_main)
def xdoctest(session):
    """Test docstring examples with xdoctest."""
    args = session.posargs or ["all"]
    session.install("--upgrade", "pip")
    session.install("xdoctest[all]", "-r", "requirements.txt")
    session.run("python", "-m", "xdoctest", package, *args)
