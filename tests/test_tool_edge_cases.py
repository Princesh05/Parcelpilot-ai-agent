from app.tools.action_tools import (
    prepare_cancellation,
    cancel_order,
    prepare_escalation,
    create_escalation
)

from app.tools.data_tools import (
    lookup_account,
    lookup_order,
    lookup_ticket
)

from app.tools.document_tools import (
    search_documents
)


# =========================================================
# TEST USERS
# =========================================================

customer_user = {
    "user_id": "user_001",
    "role": "customer",
    "account_id": "ACCT-001"
}

unauthorized_user = {
    "user_id": "user_999",
    "role": "customer",
    "account_id": "ACCT-999"
}

invalid_role_user = {
    "user_id": "user_002",
    "role": "guest",
    "account_id": "ACCT-001"
}


# =========================================================
# TEST 1: INVALID ORDER ID
# =========================================================

print("\n==============================================")
print("TEST 1: INVALID ORDER ID")
print("==============================================")

result = lookup_order(
    order_id="ORD-9999",
    user_context=customer_user
)

print("RESULT:")
print(result)

assert result["success"] is False
assert "was not found" in result["error"]

print("✅ TEST 1 PASSED")


# =========================================================
# TEST 2: UNAUTHORIZED ORDER ACCESS
# =========================================================

print("\n==============================================")
print("TEST 2: UNAUTHORIZED ORDER ACCESS")
print("==============================================")

result = lookup_order(
    order_id="ORD-1001",
    user_context=unauthorized_user
)

print("RESULT:")
print(result)

assert result["success"] is False
assert "Access denied" in result["error"]

print("✅ TEST 2 PASSED")


# =========================================================
# TEST 3: INVALID TICKET ID
# =========================================================

print("\n==============================================")
print("TEST 3: INVALID TICKET ID")
print("==============================================")

result = lookup_ticket(
    ticket_id="TKT-9999",
    user_context=customer_user
)

print("RESULT:")
print(result)

assert result["success"] is False
assert "was not found" in result["error"]

print("✅ TEST 3 PASSED")


# =========================================================
# TEST 4: INVALID ACCOUNT ID
# =========================================================

print("\n==============================================")
print("TEST 4: INVALID ACCOUNT ID")
print("==============================================")

result = lookup_account(
    account_id="ACCT-9999",
    user_context=customer_user
)

print("RESULT:")
print(result)

assert result["success"] is False

print("✅ TEST 4 PASSED")


# =========================================================
# TEST 5: CANCELLATION WITHOUT CONFIRMATION
# =========================================================

print("\n==============================================")
print("TEST 5: CANCELLATION WITHOUT CONFIRMATION")
print("==============================================")

result = cancel_order(
    order_id="ORD-1001",
    user_context=customer_user,
    confirmed=False
)

print("RESULT:")
print(result)

assert result["success"] is False
assert "confirmation is required" in result["error"]

print("✅ TEST 5 PASSED")


# =========================================================
# TEST 6: PREPARE CANCELLATION FOR INVALID ORDER
# =========================================================

print("\n==============================================")
print("TEST 6: PREPARE CANCELLATION - INVALID ORDER")
print("==============================================")

result = prepare_cancellation(
    order_id="ORD-9999",
    user_context=customer_user
)

print("RESULT:")
print(result)

assert result["success"] is False
assert "was not found" in result["error"]

print("✅ TEST 6 PASSED")


# =========================================================
# TEST 7: ESCALATION WITHOUT CONFIRMATION
# =========================================================

print("\n==============================================")
print("TEST 7: ESCALATION WITHOUT CONFIRMATION")
print("==============================================")

result = create_escalation(
    ticket_id="TKT-504",
    reason="Testing missing confirmation.",
    priority="P2",
    user_context=customer_user,
    confirmed=False
)

print("RESULT:")
print(result)

assert result["success"] is False
assert "confirmation is required" in result["error"]

print("✅ TEST 7 PASSED")


# =========================================================
# TEST 8: INVALID ESCALATION PRIORITY
# =========================================================

print("\n==============================================")
print("TEST 8: INVALID ESCALATION PRIORITY")
print("==============================================")

result = prepare_escalation(
    ticket_id="TKT-504",
    reason="Testing invalid priority.",
    priority="P5",
    user_context=customer_user
)

print("RESULT:")
print(result)

assert result["success"] is False
assert "Priority must be P1, P2, or P3" in result["error"]

print("✅ TEST 8 PASSED")


# =========================================================
# TEST 9: MISSING TICKET ID
# =========================================================

print("\n==============================================")
print("TEST 9: MISSING TICKET ID")
print("==============================================")

result = prepare_escalation(
    ticket_id="",
    reason="Testing missing ticket ID.",
    priority="P2",
    user_context=customer_user
)

print("RESULT:")
print(result)

assert result["success"] is False
assert "ticket_id is required" in result["error"]

print("✅ TEST 9 PASSED")


# =========================================================
# TEST 10: INVALID USER ROLE FOR ESCALATION
# =========================================================

print("\n==============================================")
print("TEST 10: INVALID USER ROLE FOR ESCALATION")
print("==============================================")

result = prepare_escalation(
    ticket_id="TKT-504",
    reason="Testing invalid role.",
    priority="P2",
    user_context=invalid_role_user
)

print("RESULT:")
print(result)

assert result["success"] is False
assert "not authorized" in result["error"]

print("✅ TEST 10 PASSED")


# =========================================================
# TEST 11: DOCUMENT SEARCH WITHOUT CUSTOMER ACCOUNT
# =========================================================

print("\n==============================================")
print("TEST 11: DOCUMENT SEARCH WITHOUT ACCOUNT")
print("==============================================")

customer_without_account = {
    "user_id": "user_003",
    "role": "customer"
}

result = search_documents(
    query="cancellation policy",
    user_context=customer_without_account
)

print("RESULT:")
print(result)

assert result["success"] is False
assert "Customer account context is required" in result["error"]

print("✅ TEST 11 PASSED")


# =========================================================
# FINAL RESULT
# =========================================================

print("\n==============================================")
print("🎉 ALL EDGE-CASE TESTS PASSED")
print("==============================================")