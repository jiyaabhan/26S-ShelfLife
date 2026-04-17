"""Listings — buyer/seller catalog flows (Phase 1 dummy responses)."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

listings_bp = Blueprint("listings", __name__)

_DUMMY_LISTINGS = [
    {
        "listing_id": "L-10001",
        "title": "Introduction to Algorithms (3rd ed.)",
        "course_id": "CS3000",
        "price_cents": 4200,
        "status": "active",
        "seller_user_id": "U-501",
    },
    {
        "listing_id": "L-10002",
        "title": "TI-84 Plus CE",
        "course_id": "MATH1341",
        "price_cents": 6500,
        "status": "reserved",
        "seller_user_id": "U-502",
    },
]


@listings_bp.route("/", methods=["GET", "POST"])
def list_or_create_listings():
    if request.method == "GET":
        return jsonify({"listings": _DUMMY_LISTINGS, "count": len(_DUMMY_LISTINGS)}), 200
    body = request.get_json(silent=True) or {}
    new_id = "L-99999"
    created = {
        "listing_id": new_id,
        "title": body.get("title", "Untitled listing"),
        "course_id": body.get("course_id"),
        "price_cents": body.get("price_cents", 0),
        "status": "active",
        "seller_user_id": body.get("seller_user_id", "U-000"),
    }
    return jsonify({"created": True, "listing": created}), 201


@listings_bp.route("/<listing_id>", methods=["GET"])
def get_listing(listing_id: str):
    for row in _DUMMY_LISTINGS:
        if row["listing_id"] == listing_id:
            return jsonify(row), 200
    return jsonify({"error": "not_found", "listing_id": listing_id}), 404


@listings_bp.route("/<listing_id>", methods=["PUT"])
def update_listing(listing_id: str):
    body = request.get_json(silent=True) or {}
    return (
        jsonify(
            {
                "updated": True,
                "listing_id": listing_id,
                "patch": body,
            }
        ),
        200,
    )


@listings_bp.route("/<listing_id>", methods=["DELETE"])
def delete_listing(listing_id: str):
    return jsonify({"deleted": True, "listing_id": listing_id}), 200
