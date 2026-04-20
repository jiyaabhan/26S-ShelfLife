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
