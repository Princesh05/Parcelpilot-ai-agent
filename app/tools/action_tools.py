from datetime import datetime
from pathlib import Path
import json

from app.data.service import ParcelPilotDataService
from app.data.access_control import AccessControl


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ESCALATION_FILE = PROJECT_ROOT / "data" / "escalations.json"

data_service = ParcelPilotDataService()


def _load_escalations():

    if not ESCALATION_FILE.exists():
        return []

    with open(
        ESCALATION_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def _save_escalations(escalations):

    ESCALATION_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        ESCALATION_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            escalations,
            f,
            indent=4
        )

def prepare_cancellation(
    order_id,
    user_context
):
    """
    Prepare an order cancellation.

    This function does NOT change the order.
    It only checks whether cancellation can be prepared
    and asks for explicit user confirmation.
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
            "error": (
                "Access denied. You are not authorized "
                "to cancel this order."
            )
        }

    if order["status"] != "BOOKED":
        return {
            "success": False,
            "error": (
                f"Order {order_id} cannot be cancelled "
                f"because its current status is "
                f"{order['status']}."
            )
        }

    return {
        "success": True,
        "requires_confirmation": True,
        "action": {
            "type": "cancel_order",
            "order_id": order_id
        },
        "message": (
            f"Order {order_id} is currently BOOKED and "
            "can be prepared for cancellation. "
            "Explicit user confirmation is required "
            "before the cancellation is performed."
        )
    }

def cancel_order(
    order_id,
    user_context,
    confirmed=False
):
    """
    Actually cancel an order.

    This is a state-changing operation.
    confirmed MUST be True.
    """

    if not confirmed:
        return {
            "success": False,
            "error": (
                "Explicit user confirmation is required "
                "before cancelling the order."
            )
        }

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
            "error": (
                "Access denied. You are not authorized "
                "to cancel this order."
            )
        }

    if order["status"] != "BOOKED":
        return {
            "success": False,
            "error": (
                f"Order {order_id} cannot be cancelled "
                f"because its current status is "
                f"{order['status']}."
            )
        }

    updated_order = data_service.update_order(
        order_id,
        {
            "status": "CANCELLED",
            "notes": (
                "Order cancelled after explicit "
                "user confirmation."
            )
        }
    )

    if updated_order is None:
        return {
            "success": False,
            "error": (
                f"Failed to update order {order_id}."
            )
        }

    return {
        "success": True,
        "message": (
            f"Order {order_id} was cancelled successfully."
        ),
        "data": updated_order
    }


def prepare_escalation(
    ticket_id,
    reason,
    priority,
    user_context
):
    """
    Prepare an escalation.

    IMPORTANT:
    This function does NOT change state.

    It only prepares the action for user confirmation.
    """

    role = user_context.get("role")

    if role not in [
        "customer",
        "support_agent",
        "admin"
    ]:

        return {
            "success": False,
            "error": "User is not authorized to prepare an escalation."
        }

    if not ticket_id:
        return {
            "success": False,
            "error": "ticket_id is required."
        }

    if priority not in [
        "P1",
        "P2",
        "P3"
    ]:

        return {
            "success": False,
            "error": "Priority must be P1, P2, or P3."
        }

    return {
        "success": True,
        "requires_confirmation": True,
        "action": {
            "type": "create_escalation",
            "ticket_id": ticket_id,
            "reason": reason,
            "priority": priority
        },
        "message": (
            f"Escalation prepared for ticket {ticket_id}. "
            f"Priority: {priority}. "
            "Explicit confirmation is required before creation."
        )
    }


def create_escalation(
    ticket_id,
    reason,
    priority,
    user_context,
    confirmed=False
):
    """
    Actually create an escalation.

    State-changing operation.

    confirmed MUST be True.
    """

    if not confirmed:

        return {
            "success": False,
            "error": (
                "Explicit user confirmation is required "
                "before creating an escalation."
            )
        }

    role = user_context.get("role")

    if role not in [
        "customer",
        "support_agent",
        "admin"
    ]:

        return {
            "success": False,
            "error": "User is not authorized to create an escalation."
        }

    escalations = _load_escalations()

    escalation_id = (
        f"ESC-{len(escalations) + 1:04d}"
    )

    escalation = {

        "escalation_id": escalation_id,

        "ticket_id": ticket_id,

        "reason": reason,

        "priority": priority,

        "created_by": user_context.get(
            "user_id",
            "unknown"
        ),

        "account_id": user_context.get(
            "account_id"
        ),

        "status": "open",

        "created_at": datetime.now().isoformat()
    }

    escalations.append(escalation)

    _save_escalations(escalations)

    return {
        "success": True,
        "message": "Escalation created successfully.",
        "data": escalation
    }