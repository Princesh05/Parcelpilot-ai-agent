from app.tools.data_tools import (
    lookup_account,
    lookup_order,
    lookup_ticket
)


northstar_user = {
    "user_id": "user_001",
    "role": "customer",
    "account_id": "ACCT-001"
}


support_user = {
    "user_id": "employee_001",
    "role": "support_agent",
    "account_id": None
}


print("\n========== ACCOUNT TEST ==========")

print(
    lookup_account(
        "ACCT-001",
        northstar_user
    )
)


print("\n========== ORDER TEST ==========")

print(
    lookup_order(
        "ORD-1001",
        northstar_user
    )
)


print("\n========== TICKET TEST ==========")

print(
    lookup_ticket(
        "TKT-504",
        northstar_user
    )
)


print("\n========== CROSS-ACCOUNT TEST ==========")

print(
    lookup_order(
        "ORD-2001",
        northstar_user
    )
)


print("\n========== INTERNAL SUPPORT TEST ==========")

print(
    lookup_order(
        "ORD-2001",
        support_user
    )
)