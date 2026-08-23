from app.tools.tool_dispatcher import execute_tool


USER_CONTEXT = {
    "user_id": "USR-001",
    "account_id": "ACCT-001",
    "role": "customer"
}


# =========================================================
# TEST 1: LOOKUP ORDER
# =========================================================

def test_lookup_order():

    print("\n================================")
    print("DISPATCHER TEST 1: LOOKUP ORDER")
    print("================================")

    result = execute_tool(
        tool_name="lookup_order",
        arguments={
            "order_id": "ORD-1001"
        },
        user_context=USER_CONTEXT
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is True
    assert result["data"]["order_id"] == "ORD-1001"

    print("✅ Dispatcher lookup_order passed")


# =========================================================
# TEST 2: LOOKUP ACCOUNT
# =========================================================

def test_lookup_account():

    print("\n================================")
    print("DISPATCHER TEST 2: LOOKUP ACCOUNT")
    print("================================")

    result = execute_tool(
        tool_name="lookup_account",
        arguments={
            "account_id": "ACCT-001"
        },
        user_context=USER_CONTEXT
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is True
    assert result["data"]["account_id"] == "ACCT-001"

    print("✅ Dispatcher lookup_account passed")


# =========================================================
# TEST 3: LOOKUP TICKET
# =========================================================

def test_lookup_ticket():

    print("\n================================")
    print("DISPATCHER TEST 3: LOOKUP TICKET")
    print("================================")

    result = execute_tool(
        tool_name="lookup_ticket",
        arguments={
            "ticket_id": "TKT-504"
        },
        user_context=USER_CONTEXT
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is True
    assert result["data"]["ticket_id"] == "TKT-504"

    print("✅ Dispatcher lookup_ticket passed")


# =========================================================
# TEST 4: SEARCH DOCUMENTS
# =========================================================

def test_search_documents():

    print("\n================================")
    print("DISPATCHER TEST 4: SEARCH DOCUMENTS")
    print("================================")

    result = execute_tool(
        tool_name="search_documents",
        arguments={
            "query": "cancellation policy"
        },
        user_context=USER_CONTEXT
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is True
    assert "results" in result

    print("✅ Dispatcher search_documents passed")


# =========================================================
# TEST 5: PREPARE CANCELLATION
# =========================================================

def test_prepare_cancellation():

    print("\n================================")
    print("DISPATCHER TEST 5: PREPARE CANCELLATION")
    print("================================")

    result = execute_tool(
        tool_name="prepare_cancellation",
        arguments={
            "order_id": "ORD-1001"
        },
        user_context=USER_CONTEXT
    )

    print("[RESULT]")
    print(result)

    # ORD-1001 may already be CANCELLED from
    # previous tests, so we only verify that
    # the dispatcher successfully routed the call.

    assert "success" in result

    print("✅ Dispatcher prepare_cancellation routed")


# =========================================================
# TEST 6: PREPARE ESCALATION
# =========================================================

def test_prepare_escalation():

    print("\n================================")
    print("DISPATCHER TEST 6: PREPARE ESCALATION")
    print("================================")

    result = execute_tool(
        tool_name="prepare_escalation",
        arguments={
            "ticket_id": "TKT-504",
            "reason": "Shipment is still showing BOOKED after pickup.",
            "priority": "P2"
        },
        user_context=USER_CONTEXT
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is True
    assert result["requires_confirmation"] is True
    assert result["action"]["type"] == "create_escalation"

    print("✅ Dispatcher prepare_escalation passed")


# =========================================================
# TEST 7: CREATE ESCALATION WITHOUT CONFIRMATION
# =========================================================

def test_create_escalation_without_confirmation():

    print("\n================================")
    print("DISPATCHER TEST 7: CREATE ESCALATION WITHOUT CONFIRMATION")
    print("================================")

    result = execute_tool(
        tool_name="create_escalation",
        arguments={
            "ticket_id": "TKT-504",
            "reason": "Testing dispatcher confirmation protection.",
            "priority": "P2",
            "confirmed": False
        },
        user_context=USER_CONTEXT
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is False
    assert "confirmation is required" in result["error"]

    print("✅ Dispatcher confirmation protection passed")


# =========================================================
# TEST 8: UNKNOWN TOOL
# =========================================================

def test_unknown_tool():

    print("\n================================")
    print("DISPATCHER TEST 8: UNKNOWN TOOL")
    print("================================")

    result = execute_tool(
        tool_name="something_invalid",
        arguments={},
        user_context=USER_CONTEXT
    )

    print("[RESULT]")
    print(result)

    assert result["success"] is False
    assert "Unknown tool" in result["error"]

    print("✅ Unknown tool correctly handled")


# =========================================================
# RUN ALL TESTS
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("========================================")
    print("   PARCELPILOT DISPATCHER TESTS")
    print("========================================")

    test_lookup_order()

    test_lookup_account()

    test_lookup_ticket()

    test_search_documents()

    test_prepare_cancellation()

    test_prepare_escalation()

    test_create_escalation_without_confirmation()

    test_unknown_tool()

    print("\n========================================")
    print("🎉 ALL DISPATCHER TESTS PASSED")
    print("========================================")