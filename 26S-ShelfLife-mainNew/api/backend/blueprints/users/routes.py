"""Users routes backed by real DB data."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from api.db import get_cursor

users_bp = Blueprint("users", __name__)

@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id: str):
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT user_id, name, email, is_active, avg_rating, created_at
            FROM USER
            WHERE user_id = %s
            """,
            (user_id,),
        )
        row = cur.fetchone()
    if not row:
        return jsonify({"error": "not_found", "user_id": user_id}), 404
    return jsonify(row), 200


@users_bp.route("/<user_id>/reviews", methods=["GET"])
def get_user_reviews(user_id: str):
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT review_id, listing_id, reviewer_id, seller_id, rating, comment, created_at
            FROM REVIEW
            WHERE seller_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,),
        )
        reviews = cur.fetchall()
    return (
        jsonify(
            {
                "user_id": user_id,
                "reviews": reviews,
            }
        ),
        200,
    )


@users_bp.route("/<user_id>/listings", methods=["GET"])
def get_user_listings(user_id: str):
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT l.listing_id, i.title, c.course_number, l.price, l.status, l.created_at
            FROM LISTING l
            JOIN ITEM i ON i.item_id = l.item_id
            JOIN COURSE c ON c.course_id = l.course_id
            WHERE l.user_id = %s
            ORDER BY l.created_at DESC
            """,
            (user_id,),
        )
        listings = cur.fetchall()
    return (
        jsonify(
            {
                "user_id": user_id,
                "listings": listings,
            }
        ),
        200,
    )


@users_bp.route("/<user_id>/transactions", methods=["GET"])
def get_user_transactions(user_id: str):
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
            WHERE t.buyer_id = %s OR l.user_id = %s
            ORDER BY t.sold_at DESC
            """,
            (user_id, user_id),
        )
        transactions = cur.fetchall()
    return (
        jsonify(
            {
                "user_id": user_id,
                "transactions": transactions,
            }
        ),
        200,
    )


@users_bp.route("/<user_id>/deactivate", methods=["PUT"])
def deactivate_user(user_id: str):
    body = request.get_json(silent=True) or {}
    with get_cursor() as cur:
        cur.execute(
            "UPDATE USER SET is_active = 0 WHERE user_id = %s",
            (user_id,),
        )
        changed = cur.rowcount > 0
    return (
        jsonify(
            {
                "deactivated": changed,
                "user_id": user_id,
                "reason": body.get("reason", "admin_request"),
            }
        ),
        200 if changed else 404,
    )
