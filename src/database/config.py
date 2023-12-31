"""
File: src/database/config.py

Description: Parses the database.ini file to retrieve authentication details
    for the application's database.
"""

from configparser import ConfigParser
import os
from definitions import ROOT_DIR


"""
Reads the database.ini and returns a dictionary with configuration info
"""
def config(filename=os.path.join(ROOT_DIR, "src", "database", "database.ini"), section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db