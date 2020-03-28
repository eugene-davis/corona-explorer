"""
Imports state-wise data from India
"""

import requests

from datetime import datetime
from collections import namedtuple

STATE_INFO = {
    "Andhra Pradesh": {"region_code": "AP", "pop": 0},
    "Arunachal Pradesh": {"region_code": "AR", "pop": 0},
    "Assam": {"region_code": "AS", "pop": 0},
    "Bihar": {"region_code": "BR", "pop": 0},
    "Chhattisgarh": {"region_code": "CG", "pop": 0},
    "Delhi": {"region_code": "DL", "pop": 0},
    "Goa": {"region_code": "GA", "pop": 0},
    "Gujarat": {"region_code": "GJ", "pop": 0},
    "Haryana": {"region_code": "HR", "pop": 0},
    "Himachal Pradesh": {"region_code": "HP", "pop": 0},
    "Jammu and Kashmir": {"region_code": "JK", "pop": 0},
    "Jharkhand": {"region_code": "JS", "pop": 0},
    "Karnataka": {"region_code": "KA", "pop": 0},
    "Kerala": {"region_code": "KL", "pop": 0},
    "Madhya Pradesh": {"region_code": "MP", "pop": 0},
    "Maharashtra": {"region_code": "MH", "pop": 0},
    "Manipur": {"region_code": "MN", "pop": 0},
    "Meghalaya": {"region_code": "ML", "pop": 0},
    "Mizoram": {"region_code": "MZ", "pop": 0},
    "Nagaland": {"region_code": "NL", "pop": 0},
    "Odisha": {"region_code": "OR", "pop": 0},
    "Punjab": {"region_code": "PB", "pop": 0},
    "Rajasthan": {"region_code": "RJ", "pop": 0},
    "Sikkim": {"region_code": "SK", "pop": 0},
    "Tamil Nadu": {"region_code": "TN", "pop": 0},
    "Tripura": {"region_code": "TR", "pop": 0},
    "Uttarakhand": {"region_code": "UK", "pop": 0},
    "Uttar Pradesh": {"region_code": "UP", "pop": 0},
    "West Bengal": {"region_code": "WB", "pop": 0},
    "Andaman and Nicobar Islands": {"region_code": "AN", "pop": 0},
    "Chandigarh": {"region_code": "CH", "pop": 0},
    "Dadra and Nagar Haveli": {"region_code": "DN", "pop": 0},
    "Daman and Diu": {"region_code": "DD", "pop": 0},
    "Lakshadweep": {"region_code": "LD", "pop": 0},
    "Puducherry": {"region_code": "PY", "pop": 0},
    "Telengana": {"region_code": "TG", "pop": 0},
    "Ladakh": {"region_code": "LA", "pop": 0},
}


def download_data():
    Region_Entry = namedtuple("Region", ["country_code", "region_code", "timestamp", "confirmed_cases", "deaths"])

    raw_india_data = requests.get("https://api.rootnet.in/covid19-in/stats/history")

    india_data = []

    for day_entry in raw_india_data.json()["data"]:
        timestamp = datetime.strptime(day_entry["day"], "%Y-%m-%d").timestamp()

        for region in day_entry["regional"]:
            region_entry = Region_Entry(
                country_code="IN",
                region_code=STATE_INFO[region["loc"]]["region_code"],
                timestamp=timestamp,
                confirmed_cases=region["confirmedCasesIndian"] + region["confirmedCasesForeign"],
                deaths=region["deaths"],
            )
            india_data.append(region_entry)
    return india_data
