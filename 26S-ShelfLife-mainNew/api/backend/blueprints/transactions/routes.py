"""Transactions routes backed by real DB data.

Static paths (`daily-summary`, `frequently-bought-together`) are declared before
`/<transaction_id>` so they are not captured as IDs.
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from api.db import get_cursor

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/", methods=["GET", "POST"])
def list_or_create_transactions():
    if request.method == "GET":
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT
                    t.transaction_id,
                    t.listing_id,
                    t.buyer_id,
                    l.user_id AS seller_id,
                    t.sale_price,
                    t.sold_at,
                    t.days_to_sale
                FROM `TRANSACTION` t
                JOIN LISTING l ON l.listing_id = t.listing_id
                ORDER BY t.transaction_id DESC
                """
            )
            rows = cur.fetchall()
        return jsonify({"transactions": rows, "count": len(rows)}), 200

    body = request.get_json(silent=True) or {}
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO `TRANSACTION` (listing_id, buyer_id, sale_price, sold_at, days_to_sale)
            VALUES (%s, %s, %s, NOW(), %s)
            """,
            (
                body.get("listing_id"),
                body.get("buyer_id"),
                body.get("sale_price"),
                body.get("days_to_sale"),
            ),
        )
        transaction_id = cur.lastrowid
        cur.execute(
            """
            UPDATE LISTING
            SET status = 'Sold'
            WHERE listing_id = %s
            """,
            (body.get("listing_id"),),
        )
        cur.execute(
            """
            SELECT transaction_id, listing_id, buyer_id, sale_price, sold_at, days_to_sale
            FROM `TRANSACTION`
            WHERE transaction_id = %s
            """,
            (transaction_id,),
        )
        created = cur.fetchone()
    return jsonify({"created": True, "transaction": created}), 201


@transactions_bp.route("/daily-summary", methods=["GET"])
def daily_summary():
    day = request.args.get("date")
    if not day:
        with get_cursor() as cur:
            cur.execute("SELECT DATE(MAX(sold_at)) AS latest_day FROM `TRANSACTION`")
            latest = cur.fetchone()
            day = str(latest["latest_day"]) if latest and latest["latest_day"] else None
    if not day:
        return jsonify({"error": "no_transactions"}), 404

    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                DATE(sold_at) AS date,
                COUNT(*) AS transactions_count,
                COALESCE(SUM(sale_price), 0) AS gmv
            FROM `TRANSACTION`
            WHERE DATE(sold_at) = %s
            GROUP BY DATE(sold_at)
            """,
            (day,),
        )
        row = cur.fetchone()
    if not row:
        return jsonify({"date": day, "transactions_count": 0, "gmv": 0}), 200
    return (
        jsonify(row),
        200,
    )


@transactions_bp.route("/frequently-bought-together", methods=["GET"])
def frequently_bought_together():
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                bl1.listing_id AS a,
                bl2.listing_id AS b,
                COUNT(*) AS together_count
            FROM BUNDLE_LISTING bl1
            JOIN BUNDLE_LISTING bl2
                ON bl1.bundle_id = bl2.bundle_id
               AND bl1.listing_id < bl2.listing_id
            GROUP BY bl1.listing_id, bl2.listing_id
            ORDER BY together_count DESC
            LIMIT 20
            """
        )
        pairs = cur.fetchall()
    return (
        jsonify({"pairs": pairs}),
        200,
    )


@transactions_bp.route("/<transaction_id>", methods=["GET"])
def get_transaction(transaction_id: str):
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                t.transaction_id,
                t.listing_id,
                t.buyer_id,
                l.user_id AS seller_id,
                t.sale_price,
                t.sold_at,
                t.days_to_sale
            FROM `TRANSACTION` t
            JOIN LISTING l ON l.listing_id = t.listing_id
            WHERE t.transaction_id = %s
            """,
            (transaction_id,),
        )
        row = cur.fetchone()
    if row:
        return jsonify(row), 200
    return jsonify({"error": "not_found", "transaction_id": transaction_id}), 404
