from app.data.service import ParcelPilotDataService
from app.data.access_control import AccessControl


data_service = ParcelPilotDataService()


def lookup_account(account_id, user_context):
    """
    Look up an account while enforcing access control.
    """

    if not AccessControl.can_access_account(
        user_context,
        account_id
    ):
        return {
            "success": False,
            "error": "Access denied. You are not authorized to access this account."
        }

    account = data_service.get_account(account_id)

    if account is None:
        return {
            "success": False,
            "error": f"Account {account_id} was not found."
        }

    return {
        "success": True,
        "data": account
    }


def lookup_order(order_id, user_context):
    """
    Look up an order while enforcing account-level access control.
    """

    order = data_service.get_order(order_id)

    if order is None:
        return {
            "success": False,
            "error": f"Order {order_id} was not found."
        }

    account_id = order["account_id"]

    if not AccessControl.can_access_account(
        user_context,
        account_id
    ):
        return {
            "success": False,
            "error": "Access denied. You are not authorized to access this order."
        }

    return {
        "success": True,
        "data": order
    }


def lookup_ticket(ticket_id, user_context):
    """
    Look up a support ticket while enforcing account-level access control.
    """

    ticket = data_service.get_ticket(ticket_id)

    if ticket is None:
        return {
            "success": False,
            "error": f"Ticket {ticket_id} was not found."
        }

    account_id = ticket["account_id"]

    if not AccessControl.can_access_account(
        user_context,
        account_id
    ):
        return {
            "success": False,
            "error": "Access denied. You are not authorized to access this ticket."
        }

    return {
        "success": True,
        "data": ticket
    }