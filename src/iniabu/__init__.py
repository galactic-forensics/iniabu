"""Solar System initial abundance package."""

# import the standard module as ini
from .main import IniAbu

ini = IniAbu()
inimf = IniAbu(unit="mass_fraction")
inilog = IniAbu(unit="num_log")

__all__ = ["ini", "inimf", "inilog"]
