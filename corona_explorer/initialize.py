"""
Handles the initialization of the database
"""

import sqlite3
import os
import csv
from datetime import datetime

from collections import namedtuple


def init(args):
    """
    Initialize a database then fill it
    """
    db_file = os.path.realpath(args.db)

    if args.force:
        try:
            os.remove(db_file)
        except OSError:
            pass

    if not os.path.isfile(db_file):
        conn = sqlite3.connect(db_file)
        curse = conn.cursor()
        with conn:
            create_tables(curse)
            fill_tables(curse, args.source)
    else:
        conn = sqlite3.connect(db_file)
        curse = conn.cursor()


def create_tables(curse):
    """
    Creates the corona-explorer database tables
    """
    curse.execute(
        """
        CREATE TABLE country_cases (
            timestamp INTEGER,
            country_code TEXT,
            confirmed_cases INTEGER,
            deaths INTEGER,
            temp_data INTEGER,
            PRIMARY KEY(timestamp, country_code),
            FOREIGN KEY(country_code) REFERENCES country_codes(country_code)
            )
            """
    )

    curse.execute(
        """
    CREATE TABLE country_info (
        country_code TEXT,
        country_name TEXT,
        pop INTEGER
        )
        """
    )


def fill_tables(curse, source):
    """
    Imports historical data and countries info into the database
    """
    data = []
    reader = csv.reader(source)

    for row in reader:
        data.append(row)

    import_country_info(curse, data)
    import_historical_data(curse, data)


def import_country_info(curse, data):
    """
    Fill out country_info table
    """

    Country = namedtuple("Country", ["country_name", "country_code", "pop"])
    countries = set()

    for row in data[1:]:
        country = Country(country_name=row[2], country_code=row[1], pop=row[7])
        countries.add(country)

    curse.executemany(
        """
        INSERT INTO country_info (country_name, country_code, pop)
        VALUES (?, ?, ?)
        """,
        list(countries),
    )


def import_historical_data(curse, data):
    """
    Import historical data to country_cases
    """
    historical_data = []

    Country_Entry = namedtuple("Country_Entry", ["country_code", "timestamp", "confirmed_cases", "deaths"])

    for row in data[1:]:
        if not row[4]:
            timestamp = datetime.strptime(row[0], "%Y-%m-%d").timestamp()
            country_entry = Country_Entry(
                country_code=row[1], timestamp=timestamp, confirmed_cases=int(row[5]), deaths=int(row[6])
            )

            historical_data.append(country_entry)

    curse.executemany(
        """
        INSERT INTO country_cases (country_code, timestamp, confirmed_cases, deaths, temp_data)
        VALUES (?, ?, ?, ?, 0)
        """,
        historical_data,
    )
