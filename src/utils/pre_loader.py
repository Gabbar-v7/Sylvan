from configparser import ConfigParser as _configParser
from os.path import join

config = _configParser()
config.read("config.ini")
