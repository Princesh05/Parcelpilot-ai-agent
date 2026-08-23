from .loader import load_data
import pandas as pd


class ParcelPilotDataService:

    def __init__(self):
        self.accounts, self.orders, self.tickets = load_data()

    def get_account(self, account_id):

        row = self.accounts[
            self.accounts["account_id"] == account_id
        ]

        if row.empty:
            return None

        data = row.iloc[0].to_dict()

        data = {
            key: None if pd.isna(value) else value
            for key, value in data.items()
        }

        return data

    def get_order(self, order_id):

        row = self.orders[
            self.orders["order_id"] == order_id
        ]

        if row.empty:
            return None

        data = row.iloc[0].to_dict()

        data = {
            key: None if pd.isna(value) else value
            for key, value in data.items()
        }

        return data

    def update_order(self, order_id, updates):
        """
        Update an existing order with the supplied fields.
        """

        row = self.orders.index[
            self.orders["order_id"] == order_id
        ]

        if len(row) == 0:
            return None

        index = row[0]

        for key, value in updates.items():

            if key in self.orders.columns:
                self.orders.at[index, key] = value

        return self.get_order(order_id)

    def get_ticket(self, ticket_id):

        row = self.tickets[
            self.tickets["ticket_id"] == ticket_id
        ]

        if row.empty:
            return None

        data = row.iloc[0].to_dict()

        data = {
            key: None if pd.isna(value) else value
            for key, value in data.items()
        }

        return data