"""Solar System initial abundance package."""

# import the standard module as ini
from ._version import __version__
from .main import IniAbu

ini = IniAbu()
inimf = IniAbu(unit="mass_fraction")
inilog = IniAbu(unit="num_log")

__all__ = ["ini", "inimf", "inilog", "__version__"]

__title__ = "iniabu"
__description__ = (
    "Read solar system abundances and automatically calculate various "
    "metrics, e.g., delta-values, dex, etc."
)

__uri__ = "https://iniabu.readthedocs.io/en/latest/"
__author__ = "Reto Trappitsch"
__email__ = "reto@galactic-forensics.space"

__license__ = "GPLv2"
__copyright__ = "Copyright (c) 2020-2023, Reto Trappitsch"
