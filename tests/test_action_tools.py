from app.tools.action_tools import (
    prepare_escalation,
    create_escalation
)


user = {
    "user_id": "user_001",
    "role": "customer",
    "account_id": "ACCT-001"
}


print("\n================================")
print("TEST 1: PREPARE ESCALATION")
print("================================")


result = prepare_escalation(
    ticket_id="TKT-504",
    reason="Customer reports that pickup occurred but shipment still shows BOOKED.",
    priority="P2",
    user_context=user
)


print(result)


print("\n================================")
print("TEST 2: TRY WITHOUT CONFIRMATION")
print("================================")


result = create_escalation(
    ticket_id="TKT-504",
    reason="Customer reports that pickup occurred but shipment still shows BOOKED.",
    priority="P2",
    user_context=user,
    confirmed=False
)


print(result)


print("\n================================")
print("TEST 3: CONFIRMED ACTION")
print("================================")


result = create_escalation(
    ticket_id="TKT-504",
    reason="Customer reports that pickup occurred but shipment still shows BOOKED.",
    priority="P2",
    user_context=user,
    confirmed=True
)


print(result)