from flask import Blueprint, jsonify, request
from backend.db_connection import get_db

items_bp = Blueprint("items", __name__)

@items_bp.route("/", methods=["POST"])
def create_item():
    body = request.get_json(silent=True) or {}
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        INSERT INTO ITEM (title, author, isbn, category)
        VALUES (%s, %s, %s, %s)
    ''', (
        body.get("title"),
        body.get("author"),
        body.get("isbn"),
        body.get("category"),
    ))
    get_db().commit()
    return jsonify({"item_id": cursor.lastrowid}), 201