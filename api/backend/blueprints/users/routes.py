<<<<<<< HEAD
"""Users — profiles, reviews, listings slice, transactions slice, admin deactivate (Phase 1)."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

users_bp = Blueprint("users", __name__)

_DUMMY_USER = {
    "user_id": "U-501",
    "display_name": "campus_seller_01",
    "role": "seller",
    "campus": "Northeastern University",
    "active": True,
}


@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id: str):
    row = {**_DUMMY_USER, "user_id": user_id}
    return jsonify(row), 200


@users_bp.route("/<user_id>/reviews", methods=["GET"])
def get_user_reviews(user_id: str):
    return (
        jsonify(
            {
                "user_id": user_id,
                "reviews": [
                    {
                        "review_id": "R-1",
                        "rating": 5,
                        "comment": "Fast pickup, book matched description.",
                        "counterparty_user_id": "U-777",
                    },
                    {
                        "review_id": "R-2",
                        "rating": 4,
                        "comment": "Good comms; minor highlight marks.",
                        "counterparty_user_id": "U-888",
                    },
                ],
            }
        ),
        200,
    )


@users_bp.route("/<user_id>/listings", methods=["GET"])
def get_user_listings(user_id: str):
    return (
        jsonify(
            {
                "user_id": user_id,
                "listings": [
                    {"listing_id": "L-10001", "title": "Intro to Algorithms", "status": "active"},
                    {"listing_id": "L-10040", "title": "Physics Lab Kit", "status": "sold"},
                ],
            }
        ),
        200,
    )


@users_bp.route("/<user_id>/transactions", methods=["GET"])
def get_user_transactions(user_id: str):
    return (
        jsonify(
            {
                "user_id": user_id,
                "transactions": [
                    {"transaction_id": "T-5001", "role": "seller", "amount_cents": 4200},
                    {"transaction_id": "T-5002", "role": "buyer", "amount_cents": 1800},
                ],
            }
        ),
        200,
    )


@users_bp.route("/<user_id>/deactivate", methods=["PUT"])
def deactivate_user(user_id: str):
    body = request.get_json(silent=True) or {}
    return (
        jsonify(
            {
                "deactivated": True,
                "user_id": user_id,
                "reason": body.get("reason", "admin_request"),
            }
        ),
        200,
    )
=======
from flask import Blueprint, jsonify, request
from backend.db_connection import get_db

users_bp = Blueprint("users", __name__)


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT user_id, name, email, is_active, avg_rating
        FROM USER WHERE user_id = %s
    ''', (user_id,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "not_found"}), 404
    return jsonify(result), 200


@users_bp.route("/<int:user_id>/reviews", methods=["GET"])
def get_user_reviews(user_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT r.review_id, r.rating, r.comment, r.created_at,
               u.name as reviewer
        FROM REVIEW r
        JOIN USER u ON r.reviewer_id = u.user_id
        WHERE r.seller_id = %s
        ORDER BY r.created_at DESC
    ''', (user_id,))
    return jsonify({"reviews": cursor.fetchall()}), 200


@users_bp.route("/<int:user_id>/listings", methods=["GET"])
def get_user_listings(user_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT l.listing_id, i.title, l.price, l.condition_desc,
               l.status, l.search_count, c.course_number, l.created_at
        FROM LISTING l
        JOIN ITEM i ON l.item_id = i.item_id
        JOIN COURSE c ON l.course_id = c.course_id
        WHERE l.user_id = %s
        ORDER BY l.created_at DESC
    ''', (user_id,))
    return jsonify({"listings": cursor.fetchall()}), 200


@users_bp.route("/<int:user_id>/transactions", methods=["GET"])
def get_user_transactions(user_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT t.transaction_id, t.sale_price, t.sold_at,
               i.title, l.listing_id
        FROM TRANSACTION t
        JOIN LISTING l ON t.listing_id = l.listing_id
        JOIN ITEM i ON l.item_id = i.item_id
        WHERE t.buyer_id = %s OR l.user_id = %s
        ORDER BY t.sold_at DESC
    ''', (user_id, user_id))
    return jsonify({"transactions": cursor.fetchall()}), 200


@users_bp.route("/<int:user_id>/wishlist", methods=["GET"])
def get_wishlist(user_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT w.wishlist_id, w.saved_at, l.listing_id,
               i.title, l.price, l.condition_desc,
               c.course_number, u.name as seller
        FROM WISHLIST w
        JOIN LISTING l ON w.listing_id = l.listing_id
        JOIN ITEM i ON l.item_id = i.item_id
        JOIN COURSE c ON l.course_id = c.course_id
        JOIN USER u ON l.user_id = u.user_id
        WHERE w.user_id = %s
        ORDER BY w.saved_at DESC
    ''', (user_id,))
    return jsonify({"wishlist": cursor.fetchall()}), 200


@users_bp.route("/<int:user_id>/wishlist", methods=["POST"])
def add_to_wishlist(user_id):
    body = request.get_json(silent=True) or {}
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        INSERT INTO WISHLIST (user_id, listing_id)
        VALUES (%s, %s)
    ''', (user_id, body.get("listing_id")))
    get_db().commit()
    return jsonify({"created": True, "wishlist_id": cursor.lastrowid}), 201


@users_bp.route("/<int:user_id>/wishlist/<int:wishlist_id>", methods=["DELETE"])
def remove_from_wishlist(user_id, wishlist_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        DELETE FROM WISHLIST
        WHERE wishlist_id = %s AND user_id = %s
    ''', (wishlist_id, user_id))
    get_db().commit()
    return jsonify({"deleted": True, "wishlist_id": wishlist_id}), 200


@users_bp.route("/<int:user_id>/deactivate", methods=["PUT"])
def deactivate_user(user_id):
    body = request.get_json(silent=True) or {}
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        UPDATE USER SET is_active = FALSE WHERE user_id = %s
    ''', (user_id,))
    cursor.execute('''
        UPDATE LISTING SET status = "Removed"
        WHERE user_id = %s AND status = "Active"
    ''', (user_id,))
    get_db().commit()
    return jsonify({
        "deactivated": True,
        "user_id": user_id,
        "reason": body.get("reason", "admin_request")
    }), 200


@users_bp.route("/<int:user_id>/reactivate", methods=["PUT"])
def reactivate_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        UPDATE USER SET is_active = TRUE WHERE user_id = %s
    ''', (user_id,))
    get_db().commit()
    return jsonify({"reactivated": True, "user_id": user_id}), 200
>>>>>>> b973242ce211e97bc1b86a60c6c43d1ad8a64c00
