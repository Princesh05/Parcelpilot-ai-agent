from app.tools.data_tools import lookup_order


northstar_user = {
    "user_id": "user_001",
    "role": "customer",
    "account_id": "ACCT-001"
}


print("\n--- TEST 1: OWN ACCOUNT ---")

result = lookup_order(
    "ORD-1001",
    northstar_user
)

print(result)


print("\n--- TEST 2: OTHER ACCOUNT ---")

result = lookup_order(
    "ORD-2001",
    northstar_user
)

print(result)