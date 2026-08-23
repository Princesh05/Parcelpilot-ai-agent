from app.tools.action_tools import (
    prepare_escalation,
    create_escalation
)


# =========================================================
# TEST USER
# =========================================================

northstar_user = {
    "user_id": "user_001",
    "role": "customer",
    "account_id": "ACCT-001"
}


# =========================================================
# TEST 1: PREPARE ESCALATION
# =========================================================

print("\n==============================================")
print("TEST 1: PREPARE ESCALATION")
print("==============================================")

result = prepare_escalation(
    ticket_id="TKT-504",
    reason="Customer reports that the shipment status is still BOOKED after pickup.",
    priority="P2",
    user_context=northstar_user
)

print("\nRESULT:")
print(result)


# =========================================================
# VERIFY PREPARATION
# =========================================================

assert result["success"] is True

assert result["requires_confirmation"] is True

assert result["action"]["type"] == "create_escalation"

assert result["action"]["ticket_id"] == "TKT-504"

assert result["action"]["priority"] == "P2"

print("\n✅ TEST 1 PASSED")


# =========================================================
# TEST 2: CREATE WITHOUT CONFIRMATION
# =========================================================

print("\n==============================================")
print("TEST 2: CREATE WITHOUT CONFIRMATION")
print("==============================================")

result = create_escalation(
    ticket_id="TKT-504",
    reason="Customer reports that the shipment status is still BOOKED after pickup.",
    priority="P2",
    user_context=northstar_user,
    confirmed=False
)

print("\nRESULT:")
print(result)


# =========================================================
# VERIFY SAFETY
# =========================================================

assert result["success"] is False

assert "confirmation is required" in result["error"].lower()

print("\n✅ TEST 2 PASSED")


# =========================================================
# TEST 3: CREATE WITH CONFIRMATION
# =========================================================

print("\n==============================================")
print("TEST 3: CREATE WITH CONFIRMATION")
print("==============================================")

result = create_escalation(
    ticket_id="TKT-504",
    reason="Customer reports that the shipment status is still BOOKED after pickup.",
    priority="P2",
    user_context=northstar_user,
    confirmed=True
)

print("\nRESULT:")
print(result)


# =========================================================
# VERIFY CREATION
# =========================================================

assert result["success"] is True

print("\n✅ TEST 3 PASSED")


# =========================================================
# FINAL RESULT
# =========================================================

print("\n==============================================")
print("🎉 ALL ESCALATION TESTS PASSED")
print("==============================================")