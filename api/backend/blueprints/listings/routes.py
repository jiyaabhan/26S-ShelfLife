from flask import Blueprint, jsonify, request
from backend.db_connection import get_db

listings_bp = Blueprint("listings", __name__)


@listings_bp.route("/", methods=["GET"])
def get_listings():
    cursor = get_db().cursor(dictionary=True)
    course = request.args.get("course")
    condition = request.args.get("condition")
    max_price = request.args.get("max_price")

    query = '''
        SELECT l.listing_id, i.title, i.author, i.category,
                l.price, l.condition_desc, l.status, l.search_count,
                c.course_number, u.name as seller, u.avg_rating, u.user_id as seller_id, l.course_id
        FROM LISTING l
        JOIN ITEM i ON l.item_id = i.item_id
        JOIN COURSE c ON l.course_id = c.course_id
        JOIN USER u ON l.user_id = u.user_id
        WHERE l.status = "Active"
    '''
    params = []

    if course:
        query += ' AND c.course_number LIKE %s'
        params.append(f'%{course}%')
    if condition:
        query += ' AND l.condition_desc = %s'
        params.append(condition)
    if max_price:
        query += ' AND l.price <= %s'
        params.append(max_price)

    query += ' ORDER BY l.created_at DESC'
    cursor.execute(query, params)
    return jsonify({"listings": cursor.fetchall()}), 200


@listings_bp.route("/", methods=["POST"])
def create_listing():
    body = request.get_json(silent=True) or {}
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        INSERT INTO LISTING (user_id, item_id, course_id, price, condition_desc, status)
        VALUES (%s, %s, %s, %s, %s, "Active")
    ''', (
        body.get("user_id"),
        body.get("item_id"),
        body.get("course_id"),
        body.get("price"),
        body.get("condition_desc")
    ))
    get_db().commit()
    return jsonify({"created": True, "listing_id": cursor.lastrowid}), 201


@listings_bp.route("/<int:listing_id>", methods=["GET"])
def get_listing(listing_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT l.listing_id, i.title, i.author, i.edition, i.isbn,
               i.category, l.price, l.condition_desc,
               l.status, l.created_at, l.search_count,
               c.course_number, c.course_name,
               u.name as seller, u.avg_rating, u.user_id as seller_id
        FROM LISTING l
        JOIN ITEM i ON l.item_id = i.item_id
        JOIN COURSE c ON l.course_id = c.course_id
        JOIN USER u ON l.user_id = u.user_id
        WHERE l.listing_id = %s
    ''', (listing_id,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "not_found"}), 404
    return jsonify(result), 200


@listings_bp.route("/<int:listing_id>", methods=["PUT"])
def update_listing(listing_id):
    body = request.get_json(silent=True) or {}
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        UPDATE LISTING
        SET price = %s, condition_desc = %s, status = %s
        WHERE listing_id = %s
    ''', (
        body.get("price"),
        body.get("condition_desc"),
        body.get("status"),
        listing_id
    ))
    get_db().commit()
    return jsonify({"updated": True, "listing_id": listing_id}), 200


@listings_bp.route("/<int:listing_id>", methods=["DELETE"])
def delete_listing(listing_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('DELETE FROM LISTING WHERE listing_id = %s', (listing_id,))
    get_db().commit()
    return jsonify({"deleted": True, "listing_id": listing_id}), 200


@listings_bp.route("/<int:listing_id>/reviews", methods=["GET"])
def get_listing_reviews(listing_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT r.review_id, r.rating, r.comment, r.created_at,
               u.name as reviewer
        FROM REVIEW r
        JOIN USER u ON r.reviewer_id = u.user_id
        WHERE r.listing_id = %s
        ORDER BY r.created_at DESC
    ''', (listing_id,))
    return jsonify({"reviews": cursor.fetchall()}), 200


@listings_bp.route("/<int:listing_id>/flag", methods=["POST"])
def flag_listing(listing_id):
    body = request.get_json(silent=True) or {}
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        INSERT INTO FLAG (listing_id, reason, flag_status)
        VALUES (%s, %s, "Pending")
    ''', (listing_id, body.get("reason", "Reported by user")))
    get_db().commit()
    return jsonify({"flagged": True, "flag_id": cursor.lastrowid}), 201