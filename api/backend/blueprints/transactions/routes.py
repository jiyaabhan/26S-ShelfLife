<<<<<<< HEAD
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
=======

from flask import Blueprint, jsonify, request
from backend.db_connection import get_db

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/", methods=["GET"])
def get_transactions():
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT t.transaction_id, t.sale_price, t.sold_at, t.days_to_sale,
               l.listing_id, i.title,
               buyer.name as buyer, seller.name as seller
        FROM TRANSACTION t
        JOIN LISTING l ON t.listing_id = l.listing_id
        JOIN ITEM i ON l.item_id = i.item_id
        JOIN USER buyer ON t.buyer_id = buyer.user_id
        JOIN USER seller ON l.user_id = seller.user_id
        ORDER BY t.sold_at DESC
    ''')
    return jsonify({"transactions": cursor.fetchall()}), 200


@transactions_bp.route("/", methods=["POST"])
def create_transaction():
    body = request.get_json(silent=True) or {}
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        INSERT INTO TRANSACTION (listing_id, buyer_id, sale_price, days_to_sale)
        VALUES (%s, %s, %s, %s)
    ''', (
        body.get("listing_id"),
        body.get("buyer_id"),
        body.get("sale_price"),
        body.get("days_to_sale")
    ))
    get_db().commit()

    cursor.execute('''
        UPDATE LISTING SET status = "Sold" WHERE listing_id = %s
    ''', (body.get("listing_id"),))
    get_db().commit()

    return jsonify({"created": True, "transaction_id": cursor.lastrowid}), 201
>>>>>>> b973242ce211e97bc1b86a60c6c43d1ad8a64c00


@transactions_bp.route("/daily-summary", methods=["GET"])
def daily_summary():
    day = request.args.get("date", "2026-04-16")
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT COUNT(*) as transactions_count,
               SUM(sale_price) as total_gmv,
               DATE(sold_at) as date
        FROM TRANSACTION
        WHERE DATE(sold_at) = %s
    ''', (day,))
    return jsonify(cursor.fetchone()), 200
>>>>>>> b973242ce211e97bc1b86a60c6c43d1ad8a64c00


@transactions_bp.route("/frequently-bought-together", methods=["GET"])
def frequently_bought_together():
<<<<<<< HEAD
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
=======
    course_id = request.args.get("course_id")
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT i.item_type, COUNT(t.transaction_id) as times_purchased,
               ROUND(AVG(t.sale_price), 2) as avg_sale_price
        FROM TRANSACTION t
        JOIN LISTING l ON t.listing_id = l.listing_id
        JOIN ITEM i ON l.item_id = i.item_id
        JOIN COURSE c ON l.course_id = c.course_id
        WHERE (%s IS NULL OR c.course_id = %s)
        GROUP BY i.item_type
        ORDER BY times_purchased DESC
    ''', (course_id, course_id))
    return jsonify({"pairs": cursor.fetchall()}), 200


@transactions_bp.route("/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT t.transaction_id, t.sale_price, t.sold_at, t.days_to_sale,
               l.listing_id, i.title,
               buyer.name as buyer, seller.name as seller
        FROM TRANSACTION t
        JOIN LISTING l ON t.listing_id = l.listing_id
        JOIN ITEM i ON l.item_id = i.item_id
        JOIN USER buyer ON t.buyer_id = buyer.user_id
        JOIN USER seller ON l.user_id = seller.user_id
        WHERE t.transaction_id = %s
    ''', (transaction_id,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "not_found"}), 404
    return jsonify(result), 200
>>>>>>> b973242ce211e97bc1b86a60c6c43d1ad8a64c00
