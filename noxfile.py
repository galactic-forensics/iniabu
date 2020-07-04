import nox


nox.options.sessions = "lint", "safety", "tests"

locations = "iniabu", "tests", "noxfile.py"
python_suite = ["3.8", "3.7", "3.6"]


@nox.session(python="3.8")
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python=python_suite)
def lint(session):
    args = session.posargs or locations
    session.install("-r", "dev-requirements.txt")
    session.run("flake8", *args)


@nox.session(python=python_suite)
def tests(session):
    session.install("-r", "requirements.txt", "-r", "dev-requirements.txt")
    session.run("pytest")


@nox.session(python="3.8")
def safety(session):
    session.install("safety", "-r", "requirements.txt", "-r", "dev-requirements.txt")
    session.run(
        "safety", "check", "--full-report",
    )
