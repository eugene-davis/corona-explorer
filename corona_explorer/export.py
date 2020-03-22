"""
Exports files with COVID data
"""

import csv

from pathlib import Path
from datetime import datetime

from .retrieval import fetch_country_all_data


def export(args):
    """
    Export a csv file per country with data for a given set of countries over a given date range.
    """

    for country in args.countries:
        print("Processing data for {country}".format(country=country))

        data = fetch_country_all_data(country, args.db)

        filename = "{country}.{date}.csv".format(country=country, date=datetime.utcnow().strftime("%Y-%m-%d"))
        Path(args.export_path).mkdir(parents=True, exist_ok=True)

        header = data["history"][0]._fields
        with open(Path(args.export_path, filename), "w") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(header)
            writer.writerows(data["history"])
