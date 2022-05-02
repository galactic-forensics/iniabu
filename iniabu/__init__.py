"""Solar System initial abundance package."""

# import the standard module as ini
from .main import IniAbu

ini = IniAbu()
inimf = IniAbu(unit="mass_fraction")
inilog = IniAbu(unit="num_log")

# Package information
__version__ = "1.1.1"

__title__ = "iniabu"
__description__ = (
    "Read solar system abundances and automatically calculate various "
    "metrics, e.g., delta-values, dex, etc."
)

__uri__ = "https://iniabu.readthedocs.io/en/latest/"
__author__ = "Reto Trappitsch"
__email__ = "reto@galactic-forensics.space"

__license__ = "GPLv2"
__copyright__ = "Copyright (c) 2020-2022, Reto Trappitsch"
