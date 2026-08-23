from app.tools.action_tools import (
    prepare_cancellation,
    cancel_order,
    prepare_escalation,
    create_escalation
)


USER_CONTEXT = {
    "user_id": "USR-001",
    "account_id": "ACCT-001",
    "role": "customer"
}


# ============================================================
# TEST 3: PREPARE CANCELLATION
# ============================================================

def test_prepare_cancellation():

    print("\n================================")
    print("TEST 3: PREPARE CANCELLATION")
    print("================================")

    result = prepare_cancellation(
        "ORD-1001",
        USER_CONTEXT
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is True
    assert result["requires_confirmation"] is True
    assert result["action"]["type"] == "cancel_order"

    print("✅ Prepare cancellation passed")


# ============================================================
# TEST 4: CANCEL WITHOUT CONFIRMATION
# ============================================================

def test_cancel_without_confirmation():

    print("\n================================")
    print("TEST 4: CANCEL WITHOUT CONFIRMATION")
    print("================================")

    result = cancel_order(
        "ORD-1001",
        USER_CONTEXT,
        confirmed=False
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is False
    assert "confirmation" in result["error"].lower()

    print("✅ Cancellation correctly blocked")


# ============================================================
# TEST 5: CANCEL WITH CONFIRMATION
# ============================================================

def test_cancel_with_confirmation():

    print("\n================================")
    print("TEST 5: CANCEL WITH CONFIRMATION")
    print("================================")

    result = cancel_order(
        "ORD-1001",
        USER_CONTEXT,
        confirmed=True
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is True
    assert result["data"]["status"] == "CANCELLED"

    print("✅ Cancellation successfully performed")


# ============================================================
# TEST 6: PREPARE ESCALATION
# ============================================================

def test_prepare_escalation():

    print("\n================================")
    print("TEST 6: PREPARE ESCALATION")
    print("================================")

    result = prepare_escalation(
        ticket_id="TKT-1001",
        reason="Shipment issue requires additional support.",
        priority="P2",
        user_context=USER_CONTEXT
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is True
    assert result["requires_confirmation"] is True
    assert result["action"]["type"] == "create_escalation"

    print("✅ Prepare escalation passed")


# ============================================================
# TEST 7: CREATE ESCALATION WITHOUT CONFIRMATION
# ============================================================

def test_create_escalation_without_confirmation():

    print("\n================================")
    print("TEST 7: ESCALATION WITHOUT CONFIRMATION")
    print("================================")

    result = create_escalation(
        ticket_id="TKT-1001",
        reason="Shipment issue requires additional support.",
        priority="P2",
        user_context=USER_CONTEXT,
        confirmed=False
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is False
    assert "confirmation" in result["error"].lower()

    print("✅ Escalation correctly blocked")


# ============================================================
# TEST 8: CREATE ESCALATION WITH CONFIRMATION
# ============================================================

def test_create_escalation_with_confirmation():

    print("\n================================")
    print("TEST 8: CREATE ESCALATION WITH CONFIRMATION")
    print("================================")

    result = create_escalation(
        ticket_id="TKT-1001",
        reason="Shipment issue requires additional support.",
        priority="P2",
        user_context=USER_CONTEXT,
        confirmed=True
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is True
    assert result["data"]["ticket_id"] == "TKT-1001"
    assert result["data"]["priority"] == "P2"
    assert result["data"]["status"] == "open"

    print("✅ Escalation successfully created")


# ============================================================
# RUN ALL TESTS
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("========================================")
    print("      PARCELPILOT ACTION TOOL TESTS")
    print("========================================")

    test_prepare_cancellation()

    test_cancel_without_confirmation()

    test_cancel_with_confirmation()

    test_prepare_escalation()

    test_create_escalation_without_confirmation()

    test_create_escalation_with_confirmation()

    print("\n========================================")
    print("🎉 ALL ACTION TOOL TESTS PASSED")
    print("========================================")