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
            FOREIGN KEY(country_code) REFERENCES country_info(country_code)
            )
            """
    )

    curse.execute(
        """
        CREATE TABLE regional_cases (
            timestamp INTEGER,
            country_code TEXT,
            regional_code TEXT,
            confirmed_cases INTEGER,
            deaths INTEGER,
            temp_data INTEGER,
            PRIMARY KEY(timestamp, country_code, regional_code),
            FOREIGN KEY(country_code) REFERENCES country_info(country_code),
            FOREIGN KEY(regional_code) REFERENCES region_info(regional_code)
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

    curse.execute(
        """
        CREATE TABLE region_info (
            country_code TEXT,
            region_name TEXT,
            region_code TEXT,
            pop INTEGER,
            PRIMARY KEY(country_code, region_code),
            FOREIGN KEY(country_code) REFERENCES country_info(country_code)
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
    import_region_info(curse, data)
    import_historical_country_data(curse, data)
    import_historical_regional_data(curse, data)


def import_region_info(curse, data):
    """
    Fill out region_info table
    """

    Region = namedtuple("Region", ["country_code", "region_name", "region_code", "pop"])
    regions = set()

    for row in data[1:]:
        if row[4] or row[3]:
            region = Region(
                country_code=row[1], region_name=row[4], region_code=row[3], pop=int(row[9]) if row[9] else None
            )
            regions.add(region)

    curse.executemany(
        """
        INSERT INTO region_info (country_code, region_name, region_code,  pop)
        VALUES (?, ?, ?, ?)
        """,
        list(regions),
    )


def import_country_info(curse, data):
    """
    Fill out country_info table
    """

    Country = namedtuple("Country", ["country_name", "country_code", "pop"])
    countries = set()

    for row in data[1:]:
        if not row[4] and not row[3]:
            country = Country(country_name=row[2], country_code=row[1], pop=int(row[9]) if row[9] else None)
            countries.add(country)

    curse.executemany(
        """
        INSERT INTO country_info (country_name, country_code, pop)
        VALUES (?, ?, ?)
        """,
        list(countries),
    )


def import_historical_regional_data(curse, data):
    """
    Import historical data to regional_cases
    """
    historical_data = []

    Region_Entry = namedtuple("Region", ["country_code", "region_code", "timestamp", "confirmed_cases", "deaths"])

    for row in data[1:]:
        if row[4]:
            timestamp = datetime.strptime(row[0], "%Y-%m-%d").timestamp()
            region_entry = Region_Entry(
                country_code=row[1],
                region_code=row[3],
                timestamp=timestamp,
                confirmed_cases=int(row[5]) if row[5] else 0,
                deaths=int(row[6]) if row[6] else 0,
            )

            historical_data.append(region_entry)

    curse.executemany(
        """
        INSERT INTO regional_cases (country_code, regional_code, timestamp, confirmed_cases, deaths, temp_data)
        VALUES (?, ?, ?, ?, ?, 0)
        """,
        historical_data,
    )


def import_historical_country_data(curse, data):
    """
    Import historical data to country_cases
    """
    historical_data = []

    Country_Entry = namedtuple("Country_Entry", ["country_code", "timestamp", "confirmed_cases", "deaths"])

    for row in data[1:]:
        if not row[4]:
            timestamp = datetime.strptime(row[0], "%Y-%m-%d").timestamp()
            country_entry = Country_Entry(
                country_code=row[1],
                timestamp=timestamp,
                confirmed_cases=int(row[5]) if row[5] else 0,
                deaths=int(row[6]) if row[6] else 0,
            )

            historical_data.append(country_entry)

    curse.executemany(
        """
        INSERT INTO country_cases (country_code, timestamp, confirmed_cases, deaths, temp_data)
        VALUES (?, ?, ?, ?, 0)
        """,
        historical_data,
    )
