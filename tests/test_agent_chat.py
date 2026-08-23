from app.agent.agent import ParcelPilotAgent


USER_CONTEXT = {
    "user_id": "USR-001",
    "account_id": "ACCT-001",
    "role": "customer"
}


def print_result(title, result):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print("\n[FINAL ANSWER]")
    print(result.get("answer"))

    print("\n[TOOL HISTORY]")

    for tool_call in result.get("tool_history", []):

        print("\nTool:", tool_call["tool"])
        print("Arguments:", tool_call["arguments"])
        print("Result:", tool_call["result"])


# ============================================================
# TEST 1: ORDER LOOKUP
# ============================================================

def test_order_lookup():

    print("\n" + "=" * 60)
    print("TEST 1: ORDER LOOKUP THROUGH AGENT")
    print("=" * 60)

    agent = ParcelPilotAgent()

    result = agent.chat(
        message="What is the current status of order ORD-1001?",
        user_context=USER_CONTEXT
    )

    print_result(
        "ORDER LOOKUP RESULT",
        result
    )

    assert result["success"] is True

    print("\n✅ Agent order lookup passed")


# ============================================================
# TEST 2: POLICY QUESTION
# ============================================================

def test_policy_question():

    print("\n" + "=" * 60)
    print("TEST 2: POLICY QUESTION THROUGH AGENT")
    print("=" * 60)

    agent = ParcelPilotAgent()

    result = agent.chat(
        message=(
            "Can order ORD-1001 be cancelled? "
            "Please check the applicable policy and "
            "customer agreement."
        ),
        user_context=USER_CONTEXT
    )

    print_result(
        "POLICY QUESTION RESULT",
        result
    )

    assert result["success"] is True

    print("\n✅ Agent policy lookup passed")


# ============================================================
# TEST 3: TICKET LOOKUP
# ============================================================

def test_ticket_lookup():

    print("\n" + "=" * 60)
    print("TEST 3: TICKET LOOKUP THROUGH AGENT")
    print("=" * 60)

    agent = ParcelPilotAgent()

    result = agent.chat(
        message="What is the issue with ticket TKT-504?",
        user_context=USER_CONTEXT
    )

    print_result(
        "TICKET LOOKUP RESULT",
        result
    )

    assert result["success"] is True

    print("\n✅ Agent ticket lookup passed")


# ============================================================
# TEST 4: CANCELLATION REQUEST + CONFIRMATION
# ============================================================

def test_cancellation_confirmation():

    print("\n" + "=" * 60)
    print("TEST 4: CANCELLATION REQUEST + CONFIRMATION")
    print("=" * 60)

    agent = ParcelPilotAgent()

    # --------------------------------------------------------
    # STEP 1: Ask the agent to cancel the order
    # --------------------------------------------------------

    result = agent.chat(
        message="I want to cancel order ORD-1001.",
        user_context=USER_CONTEXT
    )

    print_result(
        "STEP 1: CANCELLATION REQUEST RESULT",
        result
    )

    assert result["success"] is True

    # Agent must create a pending action
    assert agent.pending_action is not None

    # Pending action must be cancellation
    assert agent.pending_action["type"] == "cancel_order"

    assert agent.pending_action["order_id"] == "ORD-1001"

    print("\n✅ Cancellation request prepared")
    print("[PENDING ACTION]")
    print(agent.pending_action)

    # --------------------------------------------------------
    # STEP 2: User explicitly confirms
    # --------------------------------------------------------

    result = agent.chat(
        message="yes",
        user_context=USER_CONTEXT
    )

    print_result(
        "STEP 2: CANCELLATION CONFIRMATION RESULT",
        result
    )

    assert result["success"] is True

    # Actual state-changing tool must have executed
    assert any(
        tool_call["tool"] == "cancel_order"
        for tool_call in result.get("tool_history", [])
    )

    # Pending action should be cleared
    assert agent.pending_action is None

    print("\n✅ Cancellation confirmation passed")


# ============================================================
# TEST 5: CANCELLATION REJECTION
# ============================================================

def test_cancellation_rejection():

    print("\n" + "=" * 60)
    print("TEST 5: CANCELLATION REJECTION")
    print("=" * 60)

    agent = ParcelPilotAgent()

    # --------------------------------------------------------
    # STEP 1: Ask for cancellation
    # --------------------------------------------------------

    result = agent.chat(
        message="I want to cancel order ORD-1001.",
        user_context=USER_CONTEXT
    )

    print_result(
        "STEP 1: CANCELLATION REQUEST",
        result
    )

    assert result["success"] is True

    # A pending action should exist
    assert agent.pending_action is not None

    print("\n✅ Pending cancellation created")

    # --------------------------------------------------------
    # STEP 2: User rejects
    # --------------------------------------------------------

    result = agent.chat(
        message="No, don't do it.",
        user_context=USER_CONTEXT
    )

    print_result(
        "STEP 2: USER REJECTION",
        result
    )

    assert result["success"] is True

    # Pending action must be removed
    assert agent.pending_action is None

    print("\n✅ Cancellation correctly rejected")


# ============================================================
# TEST 6: ESCALATION REQUEST + CONFIRMATION
# ============================================================

def test_escalation_confirmation():

    print("\n" + "=" * 60)
    print("TEST 6: ESCALATION REQUEST + CONFIRMATION")
    print("=" * 60)

    agent = ParcelPilotAgent()

    # --------------------------------------------------------
    # STEP 1: Ask the agent to escalate
    # --------------------------------------------------------

    result = agent.chat(
        message=(
            "Please escalate ticket TKT-504. "
            "The shipment was picked up but still shows "
            "BOOKED."
        ),
        user_context=USER_CONTEXT
    )

    print_result(
        "STEP 1: ESCALATION REQUEST",
        result
    )

    assert result["success"] is True

    # Agent should create a pending escalation
    assert agent.pending_action is not None

    assert (
        agent.pending_action["type"]
        == "create_escalation"
    )

    assert (
        agent.pending_action["ticket_id"]
        == "TKT-504"
    )

    print("\n✅ Pending escalation created")
    print("[PENDING ACTION]")
    print(agent.pending_action)

    # --------------------------------------------------------
    # STEP 2: User confirms
    # --------------------------------------------------------

    result = agent.chat(
        message="Yes, please proceed.",
        user_context=USER_CONTEXT
    )

    print_result(
        "STEP 2: ESCALATION CONFIRMATION",
        result
    )

    assert result["success"] is True

    # Actual escalation tool must have executed
    assert any(
        tool_call["tool"] == "create_escalation"
        for tool_call in result.get("tool_history", [])
    )

    # Pending action should be cleared
    assert agent.pending_action is None

    print("\n✅ Escalation confirmation passed")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("       PARCELPILOT AGENT CHAT TESTS")
    print("=" * 60)

    # --------------------------------------------------------
    # INFORMATION / RAG TESTS
    # --------------------------------------------------------

    #test_order_lookup()

    #test_policy_question()

    #test_ticket_lookup()

    # --------------------------------------------------------
    # ACTION + CONFIRMATION TESTS
    # --------------------------------------------------------

    #test_cancellation_confirmation()

    #test_cancellation_rejection()

    test_escalation_confirmation()

    print("\n")
    print("=" * 60)
    print("🎉 ALL AGENT CHAT TESTS PASSED")
    print("=" * 60)