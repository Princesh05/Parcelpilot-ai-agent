from app.agent.agent import ParcelPilotAgent


USER_CONTEXT = {
    "user_id": "USR-001",
    "account_id": "ACCT-001",
    "role": "customer"
}


def test_cancellation_confirmation_flow():

    print("\n" + "=" * 60)
    print("CANCELLATION CONFIRMATION FLOW")
    print("=" * 60)

    agent = ParcelPilotAgent()

    # -----------------------------------------
    # STEP 1: Request cancellation
    # -----------------------------------------

    result1 = agent.chat(
        message="I want to cancel order ORD-1001.",
        user_context=USER_CONTEXT
    )

    print("\nSTEP 1 - CANCELLATION REQUEST")
    print(result1)

    assert result1["success"] is True

    assert agent.pending_action is not None

    print("\nPending action:")
    print(agent.pending_action)

    # -----------------------------------------
    # STEP 2: Confirm cancellation
    # -----------------------------------------

    result2 = agent.chat(
        message="Yes, cancel it.",
        user_context=USER_CONTEXT
    )

    print("\nSTEP 2 - USER CONFIRMATION")
    print(result2)

    assert result2["success"] is True

    assert agent.pending_action is None

    # -----------------------------------------
    # Verify actual cancellation
    # -----------------------------------------

    cancellation_tool_called = any(
        call["tool"] == "cancel_order"
        and call["arguments"].get("confirmed") is True
        for call in result2["tool_history"]
    )

    assert cancellation_tool_called is True

    print("\n" + "=" * 60)
    print("✅ CANCELLATION CONFIRMATION FLOW PASSED")
    print("=" * 60)


if __name__ == "__main__":

    test_cancellation_confirmation_flow()