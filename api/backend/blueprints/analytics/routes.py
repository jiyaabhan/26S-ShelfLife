python
from flask import Blueprint, jsonify, request
from backend.db_connection import get_db

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/metrics/latest", methods=["GET"])
def get_latest_metrics():
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT metric_id, active_users, total_listings, 
               total_transactions, recorded_at
        FROM PLATFORM_METRIC
        ORDER BY recorded_at DESC
        LIMIT 1
    ''')
    return jsonify(cursor.fetchone()), 200

@analytics_bp.route("/activity", methods=["GET"])
def get_activity():
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT DATE_FORMAT(sold_at, '%Y-%m-%dT%H:00:00Z') as ts,
               COUNT(*) as count
        FROM TRANSACTION
        GROUP BY ts
        ORDER BY ts DESC
        LIMIT 20
    ''')
    return jsonify({"events": cursor.fetchall()}), 200


@analytics_bp.route("/price-trends", methods=["GET"])
def get_price_trends():
    course_id = request.args.get("course_id")
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT ph.semester, ph.avg_price, i.title
        FROM PRICE_HISTORY ph
        JOIN ITEM i ON ph.item_id = i.item_id
        JOIN COURSE_ITEM ci ON i.item_id = ci.item_id
        JOIN COURSE c ON ci.course_id = c.course_id
        WHERE (%s IS NULL OR c.course_number = %s)
        ORDER BY ph.semester
    ''', (course_id, course_id))
    return jsonify({"points": cursor.fetchall()}), 200


@analytics_bp.route("/demand-gaps", methods=["GET"])
def get_demand_gaps():
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT i.title, c.course_number,
               SUM(l.search_count) as total_searches,
               COUNT(l.listing_id) as active_listings,
               ROUND(SUM(l.search_count) / COUNT(l.listing_id), 1) as ratio
        FROM LISTING l
        JOIN ITEM i ON l.item_id = i.item_id
        JOIN COURSE c ON l.course_id = c.course_id
        WHERE l.status = 'Active'
        GROUP BY i.title, c.course_number
        ORDER BY ratio DESC
        LIMIT 10
    ''')
    return jsonify({"gaps": cursor.fetchall()}), 200


@analytics_bp.route("/seller-activity", methods=["GET"])
def get_seller_activity():
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT u.name, u.avg_rating,
               COUNT(DISTINCT l.listing_id) as total_listings,
               COUNT(DISTINCT t.transaction_id) as completed_sales,
               ROUND(AVG(t.days_to_sale), 1) as avg_days_to_sale
        FROM USER u
        LEFT JOIN LISTING l ON u.user_id = l.user_id
        LEFT JOIN TRANSACTION t ON l.listing_id = t.listing_id
        GROUP BY u.user_id, u.name, u.avg_rating
        ORDER BY completed_sales DESC
    ''')
    return jsonify({"sellers": cursor.fetchall()}), 200


@analytics_bp.route("/flags", methods=["GET"])
def get_flags():
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT f.flag_id, f.reason, f.flag_status, f.flagged_at,
               l.listing_id, i.title, l.price, l.condition_desc,
               u.name as seller, u.avg_rating, u.user_id as seller_id
        FROM FLAG f
        JOIN LISTING l ON f.listing_id = l.listing_id
        JOIN ITEM i ON l.item_id = i.item_id
        JOIN USER u ON l.user_id = u.user_id
        WHERE f.flag_status = 'Pending'
        ORDER BY f.flagged_at DESC
    ''')
    return jsonify({"flags": cursor.fetchall()}), 200


@analytics_bp.route("/flags/<int:flag_id>", methods=["PUT"])
def update_flag(flag_id):
    body = request.get_json(silent=True) or {}
    cursor = get_db().cursor()
    cursor.execute('''
        UPDATE FLAG SET flag_status = %s WHERE flag_id = %s
    ''', (body.get("flag_status", "Resolved"), flag_id))
    get_db().commit()
    return jsonify({"updated": True, "flag_id": flag_id}), 200


@analytics_bp.route("/reports", methods=["POST"])
def create_report():
    body = request.get_json(silent=True) or {}
    cursor = get_db().cursor()
    cursor.execute('''
        INSERT INTO REPORT (analyst_id, filter_params, export_format)
        VALUES (%s, %s, %s)
    ''', (
        body.get("analyst_id", 1),
        body.get("filter_params", ""),
        body.get("format", "CSV")
    ))
    get_db().commit()
    return jsonify({"report_id": cursor.lastrowid, "status": "queued"}), 202


@analytics_bp.route("/departments/activity", methods=["GET"])
def get_dept_activity():
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT d.dept_name, COUNT(l.listing_id) as total_listings
        FROM LISTING l
        JOIN COURSE c ON l.course_id = c.course_id
        JOIN DEPARTMENT d ON c.dept_id = d.dept_id
        GROUP BY d.dept_name
        ORDER BY total_listings DESC
    ''')
    return jsonify({"departments": cursor.fetchall()}), 200


@analytics_bp.route("/transactions/volume", methods=["GET"])
def get_transaction_volume():
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT DATE_FORMAT(sold_at, '%b %Y') as month,
               COUNT(*) as transactions
        FROM TRANSACTION
        GROUP BY month
        ORDER BY sold_at
    ''')
    return jsonify({"volume": cursor.fetchall()}), 200
