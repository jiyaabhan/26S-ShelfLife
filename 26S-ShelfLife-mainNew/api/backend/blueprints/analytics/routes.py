"""Analytics routes backed by real DB data."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from api.db import get_cursor

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/metrics/latest", methods=["GET"])
def get_latest_metrics():
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT metric_id, active_users, total_listings, total_transactions, recorded_at
            FROM PLATFORM_METRIC
            ORDER BY recorded_at DESC
            LIMIT 1
            """
        )
        row = cur.fetchone()
    if not row:
        return jsonify({"error": "no_metrics"}), 404
    return (
        jsonify(row),
        200,
    )


@analytics_bp.route("/activity", methods=["GET"])
def get_activity():
    window = max(1, int(request.args.get("window", "30")))
    with get_cursor() as cur:
        cur.execute(
            f"""
            SELECT DATE(created_at) AS day, COUNT(*) AS listings_created
            FROM LISTING
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL {window} DAY)
            GROUP BY DATE(created_at)
            ORDER BY day DESC
            """
        )
        listing_activity = cur.fetchall()
        cur.execute(
            f"""
            SELECT DATE(sold_at) AS day, COUNT(*) AS transactions_completed
            FROM `TRANSACTION`
            WHERE sold_at >= DATE_SUB(NOW(), INTERVAL {window} DAY)
            GROUP BY DATE(sold_at)
            ORDER BY day DESC
            """
        )
        transaction_activity = cur.fetchall()
    return (
        jsonify(
            {
                "window_days": int(window),
                "listings_created": listing_activity,
                "transactions_completed": transaction_activity,
            }
        ),
        200,
    )


@analytics_bp.route("/price-trends", methods=["GET"])
def get_price_trends():
    course_id = request.args.get("course_id")
    category = request.args.get("material_type")
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                ph.item_id,
                i.title,
                i.category,
                ph.semester,
                ph.avg_price,
                ph.low_price,
                ph.high_price,
                ph.total_sales
            FROM PRICE_HISTORY ph
            JOIN ITEM i ON i.item_id = ph.item_id
            LEFT JOIN COURSE_MATERIAL cm ON cm.item_id = i.item_id
            WHERE (%s IS NULL OR cm.course_id = %s)
              AND (%s IS NULL OR i.category = %s)
            ORDER BY ph.semester, ph.item_id
            """,
            (course_id, course_id, category, category),
        )
        points = cur.fetchall()
    return (
        jsonify({"course_id": course_id, "material_type": category, "points": points}),
        200,
    )


@analytics_bp.route("/demand-gaps", methods=["GET"])
def get_demand_gaps():
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                c.course_id,
                c.course_number,
                i.item_id,
                i.title AS material,
                COALESCE(w.wishlist_count, 0) AS wanted_count,
                COALESCE(a.active_count, 0) AS available_count,
                COALESCE(w.wishlist_count, 0) - COALESCE(a.active_count, 0) AS demand_gap
            FROM COURSE_MATERIAL cm
            JOIN COURSE c ON c.course_id = cm.course_id
            JOIN ITEM i ON i.item_id = cm.item_id
            LEFT JOIN (
                SELECT l.item_id, l.course_id, COUNT(*) AS wishlist_count
                FROM WISHLIST w
                JOIN LISTING l ON l.listing_id = w.listing_id
                GROUP BY l.item_id, l.course_id
            ) w ON w.item_id = cm.item_id AND w.course_id = cm.course_id
            LEFT JOIN (
                SELECT item_id, course_id, COUNT(*) AS active_count
                FROM LISTING
                WHERE status = 'Active'
                GROUP BY item_id, course_id
            ) a ON a.item_id = cm.item_id AND a.course_id = cm.course_id
            ORDER BY demand_gap DESC, wanted_count DESC
            LIMIT 25
            """
        )
        gaps = cur.fetchall()
    return (
        jsonify({"gaps": gaps}),
        200,
    )


@analytics_bp.route("/reports", methods=["POST"])
def create_report():
    body = request.get_json(silent=True) or {}
    analyst_id = body.get("analyst_id", 1)
    filters = body.get("filters", "")
    if isinstance(filters, dict):
        filters = "; ".join(f"{k}={v}" for k, v in filters.items())
    export_format = str(body.get("format", "CSV")).upper()

    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO REPORT (analyst_id, filter_params, export_format)
            VALUES (%s, %s, %s)
            """,
            (analyst_id, filters, export_format),
        )
        report_id = cur.lastrowid
    return (
        jsonify(
            {
                "report_id": report_id,
                "status": "created",
                "format": export_format,
                "filters": filters,
            }
        ),
        201,
    )
