
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



@transactions_bp.route("/frequently-bought-together", methods=["GET"])
def frequently_bought_together():
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
