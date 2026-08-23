from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = PROJECT_ROOT / "data" / "ParcelPilot_Assessment_Data.xlsx"


def load_data():
    """
    Load all structured ParcelPilot data from the Excel workbook.
    """

    accounts = pd.read_excel(
        DATA_FILE,
        sheet_name="accounts"
    )

    orders = pd.read_excel(
        DATA_FILE,
        sheet_name="orders"
    )

    tickets = pd.read_excel(
        DATA_FILE,
        sheet_name="tickets"
    )

    return accounts, orders, tickets