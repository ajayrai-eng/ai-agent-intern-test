from app.order_tool import OrderTool


def test_valid_order():
    tool = OrderTool()

    result = tool.lookup("ORD-1007")

    assert result["success"] is True
    assert result["order_id"] == "ORD-1007"
    assert result["status"]


def test_invalid_order_format():
    tool = OrderTool()

    result = tool.lookup("1007")

    assert result["success"] is False
    assert result["error"] == "INVALID_ORDER_ID"


def test_missing_order():
    tool = OrderTool()

    result = tool.lookup("ORD-9999")

    assert result["success"] is False
    assert result["error"] == "ORDER_NOT_FOUND"


def test_missing_order_id():
    tool = OrderTool()

    result = tool.lookup("")

    assert result["success"] is False
    assert result["error"] == "ORDER_ID_REQUIRED"


def test_internal_fields_are_not_exposed():
    tool = OrderTool()

    result = tool.lookup("ORD-1007")

    assert "risk_score" not in result
    assert "warehouse_note" not in result
    assert "customer_email" not in result
    assert "customer_address" not in result