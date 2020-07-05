"""Configurations and fixtures for ``pytest``."""

import pytest

import iniabu


@pytest.fixture
def ini_default():
    """Return ``ini`` initialized with default (lodders09) database."""
    return iniabu.IniAbu()


@pytest.fixture
def ini_nist():
    """Return ``ini`` initialized with NIST database (no solar abundances)."""
    return iniabu.IniAbu(database="nist")
