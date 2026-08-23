from app.data.service import ParcelPilotDataService


def test_get_account():
    service = ParcelPilotDataService()

    account = service.get_account("ACCT-001")

    assert account is not None
    assert account["account_id"] == "ACCT-001"

    print("✅ get_account passed")


def test_get_order():
    service = ParcelPilotDataService()

    order = service.get_order("ORD-1001")

    assert order is not None
    assert order["order_id"] == "ORD-1001"

    print("✅ get_order passed")


def test_get_ticket():
    service = ParcelPilotDataService()

    ticket = service.get_ticket("TKT-504")

    assert ticket is not None
    assert ticket["ticket_id"] == "TKT-504"

    print("✅ get_ticket passed")


def test_update_order():
    service = ParcelPilotDataService()

    updated_order = service.update_order(
        "ORD-1001",
        {
            "status": "BOOKED"
        }
    )

    assert updated_order is not None
    assert updated_order["order_id"] == "ORD-1001"
    assert updated_order["status"] == "BOOKED"

    print("✅ update_order passed")


def test_invalid_account():
    service = ParcelPilotDataService()

    account = service.get_account("ACCT-999")

    assert account is None

    print("✅ invalid account handled")


def test_invalid_order():
    service = ParcelPilotDataService()

    order = service.get_order("ORD-9999")

    assert order is None

    print("✅ invalid order handled")


def test_invalid_ticket():
    service = ParcelPilotDataService()

    ticket = service.get_ticket("TKT-9999")

    assert ticket is None

    print("✅ invalid ticket handled")


if __name__ == "__main__":

    print("=" * 48)
    print("PARCELPILOT DATA SERVICE TESTS")
    print("=" * 48)

    test_get_account()
    test_get_order()
    test_get_ticket()
    test_update_order()
    test_invalid_account()
    test_invalid_order()
    test_invalid_ticket()

    print("=" * 48)
    print("🎉 ALL DATA SERVICE TESTS PASSED")
    print("=" * 48)