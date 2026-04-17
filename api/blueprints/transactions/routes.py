"""Transactions — orders/settlement summaries (Phase 1 dummy responses).

Static paths (`daily-summary`, `frequently-bought-together`) are declared before
`/<transaction_id>` so they are not captured as IDs.
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

transactions_bp = Blueprint("transactions", __name__)

_DUMMY_TXNS = [
    {
        "transaction_id": "T-5001",
        "buyer_user_id": "U-101",
        "seller_user_id": "U-501",
        "listing_id": "L-10001",
        "amount_cents": 4200,
        "status": "completed",
    },
    {
        "transaction_id": "T-5002",
        "buyer_user_id": "U-102",
        "seller_user_id": "U-502",
        "listing_id": "L-10002",
        "amount_cents": 6500,
        "status": "pending",
    },
]


@transactions_bp.route("/", methods=["GET", "POST"])
def list_or_create_transactions():
    if request.method == "GET":
        return jsonify({"transactions": _DUMMY_TXNS, "count": len(_DUMMY_TXNS)}), 200
    body = request.get_json(silent=True) or {}
    created = {
        "transaction_id": "T-99999",
        "buyer_user_id": body.get("buyer_user_id"),
        "seller_user_id": body.get("seller_user_id"),
        "listing_id": body.get("listing_id"),
        "amount_cents": body.get("amount_cents", 0),
        "status": "pending",
    }
    return jsonify({"created": True, "transaction": created}), 201


@transactions_bp.route("/daily-summary", methods=["GET"])
def daily_summary():
    day = request.args.get("date", "2026-04-16")
    return (
        jsonify(
            {
                "date": day,
                "transactions_count": 37,
                "gmv_cents": 142_500,
                "refunds_count": 1,
            }
        ),
        200,
    )


@transactions_bp.route("/frequently-bought-together", methods=["GET"])
def frequently_bought_together():
    return (
        jsonify(
            {
                "pairs": [
                    {"a": "L-10001", "b": "L-10040", "support": 0.12},
                    {"a": "L-10002", "b": "L-10050", "support": 0.09},
                ]
            }
        ),
        200,
    )


@transactions_bp.route("/<transaction_id>", methods=["GET"])
def get_transaction(transaction_id: str):
    for row in _DUMMY_TXNS:
        if row["transaction_id"] == transaction_id:
            return jsonify(row), 200
    return jsonify({"error": "not_found", "transaction_id": transaction_id}), 404
