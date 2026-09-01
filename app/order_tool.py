import json
import re


class OrderTool:
    def __init__(self, path="data/orders.json"):
        with open(path, "r", encoding="utf-8") as f:
            orders = json.load(f)

        if isinstance(orders, dict):
            orders = orders.get("orders", [])

        self.orders = {
            order["order_id"].strip().upper(): order
            for order in orders
        }

    def lookup(self, order_id):
        if not order_id:
            return {"success": False, "error": "ORDER_ID_REQUIRED"}

        order_id = order_id.strip().upper()

        if not re.fullmatch(r"ORD-\d{4}", order_id):
            return {"success": False, "error": "INVALID_ORDER_ID"}

        order = self.orders.get(order_id)

        if not order:
            return {
                "success": False,
                "error": "ORDER_NOT_FOUND",
                "order_id": order_id,
            }

        result = {
            "success": True,
            "order_id": order_id,
            "status": order.get("status"),
        }

        # Never expose stale delivery information for cancelled/returned orders.
        if order.get("status") not in {"cancelled", "returned"}:
            for field in ["carrier", "tracking_number", "estimated_delivery"]:
                if order.get(field):
                    result[field] = order[field]

        return result