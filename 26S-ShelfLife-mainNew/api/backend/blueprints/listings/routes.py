"""Listings routes backed by real DB data."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from api.db import get_cursor

listings_bp = Blueprint("listings", __name__)

@listings_bp.route("/", methods=["GET", "POST"])
def list_or_create_listings():
    if request.method == "GET":
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT
                    l.listing_id,
                    l.user_id AS seller_user_id,
                    l.item_id,
                    i.title,
                    l.course_id,
                    c.course_number,
                    l.price,
                    l.condition_desc,
                    l.status,
                    l.created_at,
                    l.search_count
                FROM LISTING l
                JOIN ITEM i ON i.item_id = l.item_id
                JOIN COURSE c ON c.course_id = l.course_id
                ORDER BY l.listing_id DESC
                LIMIT 200
                """
            )
            rows = cur.fetchall()
        return jsonify({"listings": rows, "count": len(rows)}), 200

    body = request.get_json(silent=True) or {}
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO LISTING (user_id, item_id, course_id, price, condition_desc, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                body.get("seller_user_id"),
                body.get("item_id"),
                body.get("course_id"),
                body.get("price"),
                body.get("condition_desc", "Good"),
                body.get("status", "Active"),
            ),
        )
        listing_id = cur.lastrowid
        cur.execute(
            """
            SELECT listing_id, user_id AS seller_user_id, item_id, course_id, price, condition_desc, status, created_at
            FROM LISTING
            WHERE listing_id = %s
            """,
            (listing_id,),
        )
        created = cur.fetchone()
    return jsonify({"created": True, "listing": created}), 201


@listings_bp.route("/<listing_id>", methods=["GET"])
def get_listing(listing_id: str):
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                l.listing_id,
                l.user_id AS seller_user_id,
                l.item_id,
                i.title,
                l.course_id,
                c.course_number,
                l.price,
                l.condition_desc,
                l.status,
                l.created_at,
                l.search_count
            FROM LISTING l
            JOIN ITEM i ON i.item_id = l.item_id
            JOIN COURSE c ON c.course_id = l.course_id
            WHERE l.listing_id = %s
            """,
            (listing_id,),
        )
        row = cur.fetchone()
    if row:
        return jsonify(row), 200
    return jsonify({"error": "not_found", "listing_id": listing_id}), 404


@listings_bp.route("/<listing_id>", methods=["PUT"])
def update_listing(listing_id: str):
    body = request.get_json(silent=True) or {}
    with get_cursor() as cur:
        cur.execute(
            """
            UPDATE LISTING
            SET price = COALESCE(%s, price),
                condition_desc = COALESCE(%s, condition_desc),
                status = COALESCE(%s, status),
                course_id = COALESCE(%s, course_id)
            WHERE listing_id = %s
            """,
            (
                body.get("price"),
                body.get("condition_desc"),
                body.get("status"),
                body.get("course_id"),
                listing_id,
            ),
        )
        updated = cur.rowcount > 0
    return (
        jsonify(
            {
                "updated": updated,
                "listing_id": listing_id,
                "patch": body,
            }
        ),
        200 if updated else 404,
    )


@listings_bp.route("/<listing_id>", methods=["DELETE"])
def delete_listing(listing_id: str):
    with get_cursor() as cur:
        cur.execute("DELETE FROM LISTING WHERE listing_id = %s", (listing_id,))
        deleted = cur.rowcount > 0
    return jsonify({"deleted": deleted, "listing_id": listing_id}), (200 if deleted else 404)
