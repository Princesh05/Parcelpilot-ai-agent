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


def test_prepare_cancellation():

    result = prepare_cancellation(
        order_id="ORD-1001",
        user_context=USER_CONTEXT
    )

    print("\nPREPARE CANCELLATION")
    print(result)

    assert result["success"] is True
    assert result["requires_confirmation"] is True


def test_cancel_without_confirmation():

    result = cancel_order(
        order_id="ORD-1001",
        user_context=USER_CONTEXT,
        confirmed=False
    )

    print("\nCANCEL WITHOUT CONFIRMATION")
    print(result)

    assert result["success"] is False


def test_prepare_escalation():

    result = prepare_escalation(
        ticket_id="TKT-504",
        reason="Customer requires urgent assistance",
        priority="P2",
        user_context=USER_CONTEXT
    )

    print("\nPREPARE ESCALATION")
    print(result)

    assert result["success"] is True
    assert result["requires_confirmation"] is True


def test_create_escalation_without_confirmation():

    result = create_escalation(
        ticket_id="TKT-504",
        reason="Customer requires urgent assistance",
        priority="P2",
        user_context=USER_CONTEXT,
        confirmed=False
    )

    print("\nCREATE ESCALATION WITHOUT CONFIRMATION")
    print(result)

    assert result["success"] is False


if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("PARCELPILOT ACTION TOOL TESTS")
    print("=" * 60)

    test_prepare_cancellation()
    test_cancel_without_confirmation()
    test_prepare_escalation()
    test_create_escalation_without_confirmation()

    print("\n" + "=" * 60)
    print("ALL ACTION TOOL TESTS PASSED")
    print("=" * 60)